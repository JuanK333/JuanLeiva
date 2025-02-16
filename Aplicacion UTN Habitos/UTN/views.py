
from PyQt5.QtWidgets import (
    QMainWindow, QPushButton, QVBoxLayout, QWidget, 
    QLineEdit, QLabel, QListWidget, QMessageBox, QTextEdit
)
from PyQt5.QtWidgets import QMessageBox
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import date
import numpy as np
import logging
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from logg import ServerThread, LogReaderThread
from cliente import send_data

class HabitView(QMainWindow):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.complete_button = QPushButton("Marcar como Terminado", self)
        self.complete_button.clicked.connect(lambda: self.controller.mark_habit_completed(self))
        self.first_done_button = QPushButton("Marcar como Hecho", self)
        self.first_done_button.clicked.connect(lambda: self.controller.mark_first_time(self.habit_list, self))
        self.init_ui()

    

    def init_ui(self):
        self.setWindowTitle("Entrenador de Hábitos")
        self.setGeometry(100, 100, 500, 600)
        self.activity_log = [] 
        layout = QVBoxLayout()

        self.title_label = QLabel("Entrenador de Hábitos", self)
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("font-size: 20px; font-weight: bold;")
        layout.addWidget(self.title_label)

        # Agregar una imagen
        self.image_label = QLabel(self)
        pixmap = QPixmap("/home/juan/VC/UTN/download.jpeg")
        pixmap = pixmap.scaled(600, 500, Qt.KeepAspectRatio) 
        self.image_label.setPixmap(pixmap)
        self.image_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.image_label)

        self.habit_input = QLineEdit(self)
        self.habit_input.setPlaceholderText("Escribe un nuevo hábito...")
        layout.addWidget(self.habit_input)

        self.add_button = QPushButton("Agregar Hábito", self)
        self.add_button.clicked.connect(self.add_habit)
        layout.addWidget(self.add_button)

        self.habit_list = QListWidget(self)
        layout.addWidget(self.habit_list)

         # Boton para marcar como hecho 
        #self.first_done_button = QPushButton("Marcar como Hecho", self)
        #self.first_done_button.clicked.connect(self.get_selected_habit)
        self.first_done_button.setToolTip("Este boton marca habito como hecho una vez y le agrega 10 puntos de valor")
        
        layout.addWidget(self.first_done_button)

        self.daily_progress_button = QPushButton("Mostrar el progreso total del día", self)
        self.daily_progress_button.clicked.connect(self.show_daily_progress)
        layout.addWidget(self.daily_progress_button)

        # Boton para marcar hábito como completado
        #self.complete_button = QPushButton("Marcar como Terminado", self)
        #self.complete_button.clicked.connect(self.controller.mark_habit_completed)
        self.complete_button.setToolTip("Este boton marca habito como completado y lo borra de la lista de habitos")
        layout.addWidget(self.complete_button)

        # Boton para Mostrar habitos incompletos del dia
        self.add_button = QPushButton("Mostrar habitos incompletos del dia", self)
        self.add_button.clicked.connect(self.show_incomplete_habits)
        layout.addWidget(self.add_button)

        # Boton para mostrar gráficos
        self.graph_button = QPushButton("Ver Progreso", self)
        self.graph_button.clicked.connect(self.show_progress)
        self.graph_button.setToolTip("Este boton muestra el progreso de un  habito en un grafico")
        layout.addWidget(self.graph_button)


        # Boton para mostrar el nivel de usuario
        self.level_button = QPushButton("Ver Mi Nivel", self)
        self.level_button.clicked.connect(self.display_user_level)
        self.level_button.setToolTip("Muestra tu nivel actual basado en los puntos totales acumulados")
        layout.addWidget(self.level_button)
        
        # Boton para mostrar gráficos avanzados
        self.graphs_button = QPushButton("Ver Graficos Avanzados", self)
        self.graphs_button.clicked.connect(self.show_additional_graphs)
        self.graphs_button.setToolTip("Este boton muestra graficos de la evolucion de todos tus habitos")
        layout.addWidget(self.graphs_button)

        # Boton para mostrar prediccion
        self.prediction_button = QPushButton("Predecir Progreso Futuro", self)
        self.prediction_button.clicked.connect(self.show_future_progress)
        self.prediction_button.setToolTip("Este boton crea una serie predictora de la evolucion de un habito por 1 semana en base al historial actual de un habito")
        layout.addWidget(self.prediction_button)


        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
        self.load_habits()

        # Crear el área de texto para mostrar los mensajes
        self.text_area = QTextEdit(self)
        self.text_area.setReadOnly(True)
        self.message_input = QLineEdit(self)

        layout.addWidget(self.text_area)

        self.server_thread = QPushButton("Iniciar servidor", self)
        self.server_thread.clicked.connect(self.start_server)
        layout.addWidget(self.server_thread)
        
        self.send_button = QPushButton("Enviar log de actividad", self)
        self.send_button.clicked.connect(self.send_activity_log)
        layout.addWidget(self.send_button)


        def display_message(self, message):
            self.text_area.append(message)

        # Botón para iniciar el servidor
        #self.start_server_button = QPushButton("Iniciar Servidor", self)
        #self.start_server_button.clicked.connect(iniciar_servidor)
        #layout.addWidget(self.start_server_button)
        
        # Botón para ejecutar el cliente
        #self.start_client_button = QPushButton("Enviar Log", self)
        #self.start_client_button.clicked.connect(ejecutar_cliente)
        #layout.addWidget(self.start_client_button)

    def add_habit(self):
        self.log_activity("Habito agregado")
        habit_name = self.habit_input.text().strip()
        if habit_name:
            self.controller.add_habit(habit_name)
            self.habit_input.clear()
            self.load_habits()

    def load_habits(self):
            self.log_activity("Habito cargado")
            habits = self.controller.get_habits()
            self.habit_list.clear()
            for habit_id, habit_name in habits:
                self.habit_list.addItem(habit_name)
        
    def show_daily_progress(self):
        self.log_activity("progreso diario agregado")
        message = self.controller.show_daily_progress()
        QMessageBox.information(self, "Progreso del Día", message)

    def show_message(self, title, message, info=False):
        if info:
            QMessageBox.information(None, title, message)
        else:
            QMessageBox.warning(None, title, message)

    def remove_habit_from_list(self, selected_item):
        self.log_activity("Habito removido")
        row = self.habit_list.row(selected_item)
        self.habit_list.takeItem(row)

    def show_progress(self):
        self.log_activity("Progreso mostrado")
        # Obtener el hábito seleccionado
        selected_item = self.habit_list.currentItem()
        if not selected_item:
            QMessageBox.warning(self, "Error", "No has seleccionado un hábito.")
            return
        
        habit_name = selected_item.text()
        
        # Llamar al controlador para obtener los datos del progreso
        (dates, points), error = self.controller.get_progress_for_habit(habit_name)

        if error:
            QMessageBox.warning(self, "Error", error)
        else:
            self.plot_progress(habit_name, dates, points)

    def plot_progress(self, habit_name, dates, points):
        plt.figure(figsize=(8, 5))
        plt.plot(dates, points, marker="o", color="skyblue")
        plt.title(f"Progreso de Puntos para '{habit_name}'")
        plt.xlabel("Fecha")
        plt.ylabel("Puntos")
        plt.grid()
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d %b %Y'))  
        plt.gca().xaxis.set_major_locator(mdates.MonthLocator())  

        plt.xticks(rotation=45) 
        plt.tight_layout()
        plt.show()

    def show_additional_graphs(self):
        self.log_activity("Mostrado graficso adicionales")
        """Muestra gráficos adicionales basados en datos obtenidos del controlador."""
        dates, habits, habit_points, error = self.controller.get_additional_progress()

        if error:
            self.show_message("Error", error)  # Mostrar un mensaje en caso de error
            return

        if not dates or not habits:
            self.show_message("Información", "No hay datos disponibles para mostrar.")
            return

        # Generar gráficos si los datos están disponibles
        self.plot_additional_graphs(dates, habits, habit_points)

    def plot_additional_graphs(self, dates, habits, habit_points):
        """Generar y mostrar los gráficos adicionales."""

        # Gráfico de barras con puntos por hábito en cada fecha
        fig, ax = plt.subplots(figsize=(8, 5))
        bar_width = 0.2
        for i, habit in enumerate(habits):
            ax.bar(
                np.array([mdates.date2num(date) for date in dates]) + (i - len(habits) / 2) * bar_width,
                habit_points[habit],
                width=bar_width,
                label=f'Hábito {habit}'
            )
        ax.set_xticks([mdates.date2num(date) for date in dates])
        ax.set_xticklabels([date.strftime('%d %b %Y') for date in dates], rotation=45)
        ax.set_title("Progreso de Puntos por Hábito")
        ax.set_xlabel("Fecha")
        ax.set_ylabel("Puntos")
        ax.legend()
        plt.tight_layout()
        plt.show()

        # Gráfico de líneas para todos los hábitos
        plt.figure(figsize=(8, 5))
        for habit in habits:
            plt.plot(dates, habit_points[habit], marker="o", label=f'Hábito {habit}')
        plt.title("Progreso de Puntos por Hábito (Líneas)")
        plt.xlabel("Fecha")
        plt.ylabel("Puntos")
        plt.legend()
        plt.grid()
        plt.tight_layout()
        plt.show()
    
    def show_incomplete_habits(self):
        self.log_activity("MOstrado habitos completos")
        # Llamar al controlador para obtener los hábitos incompletos
        today = date.today()
        incomplete_habits, error = self.controller.get_incomplete_habits(today)

        if error:
            QMessageBox.warning(self, "Error", error)
        else:
            if incomplete_habits:
                habits_message = "Hábitos pendientes de completar hoy:\n"
                for habit in incomplete_habits:
                    habits_message += f"- {habit[0]}\n"
                QMessageBox.information(self, "Hábitos Pendientes", habits_message)
            else:
                QMessageBox.information(self, "Hábitos Pendientes", "¡Todos tus hábitos han sido completados hoy!")

    def show_future_progress(self):
        self.log_activity("MOstrado prediccion")
        # Llamar al controlador para obtener la predicción
        selected_item = self.habit_list.currentItem()
        if not selected_item:
            QMessageBox.warning(self, "Error", "Por favor, selecciona un hábito primero.")
            return

        habit_name = selected_item.text()

        future_dates, future_predictions, error = self.controller.predict_future_progress(habit_name)

        if error:
            QMessageBox.warning(self, "Error", error)
        else:
            prediction_message = f"Predicción del progreso para los próximos 7 días en el hábito: {habit_name}:\n"
            for i, prediction in enumerate(future_predictions, 1):
                prediction_message += f"Fecha: {future_dates[i-1]} - Predicción de puntos: {prediction:.2f}\n"
            
            QMessageBox.information(self, "Predicción de Progreso Futuro", prediction_message)

    def display_user_level(self):
        self.log_activity("Mostrado nivel de usuario")
        """Muestra el nivel actual del usuario."""
        total_points, level, points_needed, error = self.controller.get_user_level_info()

        if error:
            QMessageBox.warning(self, "Error", error)
        else:
            if points_needed is not None:
                message = (f"¡Tu nivel actual es: {level}!\n"
                           f"Puntos totales: {total_points}\n"
                           f"Te faltan {points_needed} puntos para el siguiente nivel.")
            else:
                message = (f"¡Felicitaciones! Has alcanzado el nivel de {level}!\n"
                           f"Puntos totales: {total_points}\n"
                           "¡Has alcanzado el máximo nivel!")
            
            QMessageBox.information(self, "Nivel de Usuario", message)

    def show_habit_marked_message(self, habit_name):
        """Muestra un mensaje de éxito al marcar un hábito como completado."""
        QMessageBox.information(self, "¡Logro!", f"¡Hecho una vez: {habit_name}!")

    def show_error_message(self, error):
        """Muestra un mensaje de error."""
        QMessageBox.warning(self, "Error", error)

    def get_selected_habit(self, habit_list):
        """Obtiene el hábito seleccionado de la lista."""
        selected_item = habit_list.currentItem()
        if not selected_item:
            self.show_error_message("No hay ningún hábito seleccionado.")
            return None
        return selected_item.text()
    
    def show_notification(self, message):
        """Muestra una notificación al usuario."""
        QMessageBox.information(None, "Recordatorio", message)

    def display_message(self, message):
        """Muestra un mensaje motivacional en un cuadro de diálogo."""
        QMessageBox.information(None, "Mensaje de motivación", message)

    
    def start_server(self):
        self.server_thread = ServerThread()
        self.server_thread.message_received.connect(self.display_message)
        self.server_thread.start()

        # Registrar la actividad del usuario al iniciar el servidor
        self.log_activity("Servidor iniciado")

        # Iniciar el hilo para leer el archivo de log
        self.log_reader_thread = LogReaderThread()
        self.log_reader_thread.log_update_signal.connect(self.display_message)
        self.log_reader_thread.start()

    def send_activity_log(self):
        # Enviar el registro de actividad al servidor
        if self.activity_log:
            log_message = "\n".join(self.activity_log)
            send_data(log_message)  # Enviar el registro completo de actividad
            self.text_area.append(f"Registro de actividad enviado al servidor:\n{log_message}")
        else:
            self.text_area.append("No hay registros de actividad para enviar.")

    def log_activity(self, activity):
        # Registrar una nueva actividad en el archivo de log (server.log)self.first_done_button.log_activity("habito dado")
        self.activity_log.append(activity)
        logging.info(activity)  # Escribir en el archivo de log
        print(f"Actividad registrada: {activity}")

    def display_message(self, message):
        # Mostrar el mensaje recibido o el log en el área de texto
        self.text_area.append(message)

    def closeEvent(self, event):
        # Detener los hilos cuando se cierre la ventana
        if hasattr(self, 'server_thread'):
            self.server_thread.stop()
        if hasattr(self, 'log_reader_thread'):
            self.log_reader_thread.stop()
        event.accept()