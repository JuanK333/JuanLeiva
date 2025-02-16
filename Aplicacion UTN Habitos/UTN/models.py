import sys
import psycopg2
from observers import Tema
from datetime import date, timedelta, datetime
import random
import numpy as np
from sklearn.linear_model import LinearRegression
from decorators import retry



class HabitModel(Tema):
    def __init__(self, db_config):
        self.db_config = db_config
        super().__init__()  # Inicializa la lista de observadores


    @retry(retries=5, delay=2)
    def connect_to_db(self):
        try:
            conn = psycopg2.connect(**self.db_config)
            return conn
        except Exception as e:
            print("Error al conectar con la base de datos:", e)
            sys.exit(1)

    def initialize_db(self):
        conn = self.connect_to_db()
        with conn.cursor() as cur:
            cur.execute("""
            CREATE TABLE IF NOT EXISTS habits (
                id SERIAL PRIMARY KEY,
                name TEXT UNIQUE NOT NULL,
                is_first_done BOOLEAN DEFAULT FALSE
            );
            CREATE TABLE IF NOT EXISTS progress (
                id SERIAL PRIMARY KEY,
                habit_id INTEGER REFERENCES habits(id),
                date DATE NOT NULL,
                points INTEGER NOT NULL
            );
            """)
            conn.commit()
        conn.close()

    def add_habit(self, habit_name):
        conn = self.connect_to_db()
        try:
            with conn.cursor() as cur:
                cur.execute("INSERT INTO habits (name) VALUES (%s) ON CONFLICT DO NOTHING;", (habit_name,))
                conn.commit()
                self.notificar(f"Hábito '{habit_name}' agregado.")  # Notificar a los observadores
        except Exception as e:
            print(f"Error al agregar hábito: {e}")
        conn.close()

    def get_habits(self):
        conn = self.connect_to_db()
        habits = []
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT id, name FROM habits;")
                habits = cur.fetchall()
        except Exception as e:
            print(f"Error al obtener hábitos: {e}")
        conn.close()
        return habits

    def show_daily_progress(self):
        today = date.today()
        conn = self.connect_to_db()
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT habits.name, SUM(progress.points) 
                    FROM progress
                    JOIN habits ON progress.habit_id = habits.id
                    WHERE progress.date = %s
                    GROUP BY habits.name;
                """, (today,))
                return cur.fetchall()
        except Exception as e:
            raise Exception(f"No se pudo obtener el progreso del día: {e}")
        finally:
            conn.close()


    def delete_habit(self, habit_name):
        """Elimina un hábito por su nombre."""
        conn = self.connect_to_db()
        if conn is None:
            print("No se pudo establecer la conexión con la base de datos.")
            return False

        try:
            with conn.cursor() as cur:
                cur.execute("SELECT id FROM habits WHERE name = %s;", (habit_name,))
                habit_id = cur.fetchone()
                if habit_id:
                    cur.execute("DELETE FROM habits WHERE id = %s;", (habit_id[0],))
                    conn.commit()
                    self.notificar(f"Habito '{habit_name}' completado y eliminado de la aplicacion.")  # Notificar a los observadores
                    return True
                return False
        except Exception as e:
            print(f"Error al eliminar el hábito: {e}")
            return False
        finally:
            conn.close()

        
    def get_habit_progress(self, habit_name):
        conn = self.connect_to_db()
        try:
            with conn.cursor() as cur:
                # Obtener el id del hábito
                cur.execute("SELECT id FROM habits WHERE name = %s;", (habit_name,))
                habit_id = cur.fetchone()
                
                if not habit_id:
                    return None, f"No se encontró el hábito '{habit_name}'."
                
                # Consultar el progreso del hábito específico
                cur.execute("""
                    SELECT date, SUM(points) 
                    FROM progress 
                    WHERE habit_id = %s
                    GROUP BY date 
                    ORDER BY date;
                """, (habit_id[0],))
                data = cur.fetchall()

                if not data:
                    return None, f"No hay datos de progreso para el hábito '{habit_name}'."
                
                dates = [row[0] for row in data]
                points = [row[1] for row in data]
                
                return (dates, points), None  # Devuelve los datos y ningún mensaje de error
        except Exception as e:
            return None, f"No se pudo cargar el progreso: {e}"
        finally:
            conn.close()

    def get_habit_progress_data(self):
        """Obtiene las fechas, nombres de los hábitos y puntos de progreso."""
        conn = self.connect_to_db()
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT habits.name, progress.date, SUM(progress.points)
                    FROM progress
                    JOIN habits ON habits.id = progress.habit_id
                    GROUP BY habits.name, progress.date
                    ORDER BY progress.date;
                """)
                data = cur.fetchall()
                # Organizar los datos en un formato usable
                habit_points = {}
                dates = set()
                habit_names = set()
                for habit_name, date, points in data:
                    dates.add(date)
                    habit_names.add(habit_name)
                    if habit_name not in habit_points:
                        habit_points[habit_name] = []
                    habit_points[habit_name].append((date, points))

                # Ordenar fechas y estructurar puntos
                dates = sorted(dates)
                for habit_name in habit_points:
                    points_by_date = {date: points for date, points in habit_points[habit_name]}
                    habit_points[habit_name] = [points_by_date.get(date, 0) for date in dates]

                return dates, sorted(habit_names), habit_points, None  # Agregar un cuarto valor para el error
        except Exception as e:
            print(f"Error al obtener los datos de progreso: {e}")
            return [], [], {}, f"Error al obtener datos: {e}"
        finally:
            conn.close()

    def get_incomplete_habits(self, today):
        """Obtiene los hábitos que no se han completado hoy."""
        conn = self.connect_to_db()
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT habits.name
                    FROM habits
                    LEFT JOIN progress ON habits.id = progress.habit_id 
                    AND progress.date = %s
                    WHERE progress.habit_id IS NULL;
                """, (today,))
                return cur.fetchall(), None
        except Exception as e:
            return None, f"No se pudo verificar los hábitos: {e}"
        finally:
            conn.close()
        
    def get_historical_data(self, habit_name):
        """Obtiene los datos históricos de progreso para un hábito específico."""
        conn = self.connect_to_db()
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT date, SUM(points)
                    FROM progress
                    JOIN habits ON habits.id = progress.habit_id
                    WHERE habits.name = %s
                    GROUP BY date
                    ORDER BY date;
                """, (habit_name,))
                return cur.fetchall(), None
        except Exception as e:
            return None, f"No se pudo obtener los datos históricos para el hábito: {e}"
        finally:
            conn.close()

    def predict_future_progress(self, habit_name):
        """Predice el progreso futuro de un hábito usando regresión lineal."""
        data, error = self.get_historical_data(habit_name)
        if error:
            return None, error

        if not data:
            return None, f"No hay datos de progreso para el hábito: {habit_name}."

        # Convertir fechas a números (en formato Unix timestamp) para la regresión lineal
        dates = [row[0] for row in data]
        points = [row[1] for row in data]

        # Convertir las fechas a enteros (en milisegundos) para la regresión
        dates_int = np.array([int(datetime.combine(d, datetime.min.time()).timestamp()) for d in dates]).reshape(-1, 1)
        points = np.array(points)

        # Crear el modelo de regresión lineal
        model = LinearRegression()

        # Ajustar el modelo a los datos históricos
        model.fit(dates_int, points)

        # Predecir el progreso para los próximos 7 días
        future_dates = [date.today() + timedelta(days=i) for i in range(1, 8)]
        future_dates_int = np.array([int(datetime.combine(d, datetime.min.time()).timestamp()) for d in future_dates]).reshape(-1, 1)
        future_predictions = model.predict(future_dates_int)

        return future_dates, future_predictions, None
    
    def get_total_points(self):
        
        conn = self.connect_to_db()
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT COALESCE(SUM(points), 0) as total_points
                    FROM progress;
                """)
                total_points = cur.fetchone()[0]
                return total_points, None
        except Exception as e:
            return None, f"No se pudo obtener los puntos totales: {e}"
        finally:
            conn.close()

    @staticmethod
    def get_user_level(points):
        """Determina el nivel del usuario basado en los puntos."""
        if points >= 2000:
            return "Maestro"
        elif points >= 1000:
            return "Experto"
        elif points >= 500:
            return "Intermedio"
        else:
            return "Principiante"

    @staticmethod
    def get_next_level_points(level):
        """Obtiene los puntos necesarios para alcanzar el siguiente nivel."""
        next_level_points = {
            "Principiante": 500,
            "Intermedio": 1000,
            "Experto": 2000,
            "Maestro": None
        }
        return next_level_points[level]
    
    def get_habit_data(self, habit_name):
        """Obtiene la información de un hábito por su nombre."""
        conn = self.connect_to_db()
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT id, is_first_done FROM habits WHERE name = %s;", (habit_name,))
                habit_data = cur.fetchone()
                return habit_data, None
        except Exception as e:
            return None, f"No se pudo obtener el hábito: {e}"
        finally:
            conn.close()

    def mark_first_done(self, habit_id):
        """Marca un hábito como completado por primera vez y agrega puntos."""
        conn = self.connect_to_db()  # Obtener la conexión a la base de datos
        if conn is None:
            print("No se pudo establecer la conexión con la base de datos.")
            return "Error al conectar a la base de datos."

        try:
            with conn.cursor() as cur:
                # Actualizar el hábito para marcarlo como hecho por primera vez
                cur.execute("""
                    UPDATE habits SET is_first_done = TRUE WHERE id = %s;
                    INSERT INTO progress (habit_id, date, points) VALUES (%s, %s, %s);
                """, (habit_id, habit_id, date.today(), 10))
                conn.commit()  # Confirmar los cambios en la base de datos
                
                return None  # Sin errores
        except Exception as e:
            print(f"Error al actualizar el hábito: {e}")
            return f"No se pudo actualizar el hábito: {e}"
        finally:
            conn.close()

  
    def get_random_message(self):
        """Devuelve un mensaje motivacional aleatorio."""
        self.messages = [
            "¡Sigue así, estás logrando grandes cosas!",
            "Cada pequeño paso cuenta, ¡sigue avanzando!",
            "¡Estás más cerca de tu meta, no te detengas!",
        ]
        return random.choice(self.messages)