from PyQt5.QtCore import Qt, QTimer
from decorators import validate_arguments, measure_time

class HabitController:
    def __init__(self, model):
        self.model = model
        
    @measure_time   
    @validate_arguments(arg_types=[str])
    def add_habit(self, habit_name):
        self.model.add_habit(habit_name)

    def get_habits(self):
        return self.model.get_habits()
    
    
    @measure_time
    def show_daily_progress(self):
        try:
            progress_data = self.model.show_daily_progress()
            if progress_data:
                progress_message = "Progreso del Día:\n"
                for habit_name, points in progress_data:
                    progress_message += f"{habit_name}: {points} puntos\n"
            else:
                progress_message = "No hay progreso registrado para hoy."
            return progress_message
        except Exception as e:
            return str(e)
        
    def mark_habit_completed(self, view):
        selected_item = view.habit_list.currentItem()
        if selected_item:
            habit = selected_item.text()
            if self.model.delete_habit(habit):
                view.remove_habit_from_list(selected_item)
                #view.show_message("Hábito Eliminado", f"¡El hábito '{habit}' ha sido eliminado y completado!", info=True)
            else:
                view.show_message("Error", f"No se pudo marcar el hábito '{habit}' como completado.")
        else:
            view.show_message("Error", "No hay ningún hábito seleccionado.")

    def get_progress_for_habit(self, habit_name):
        # Obtener el progreso del hábito desde el modelo
        return self.model.get_habit_progress(habit_name)
    
    def get_additional_progress(self):
        # Obtener los datos de progreso adicional del modelo
        return self.model.get_habit_progress_data()
    
    def get_incomplete_habits(self, today):
        # Obtener los hábitos incompletos del modelo
        return self.model.get_incomplete_habits(today)
    
    def predict_future_progress(self, habit_name):
        # Obtener la predicción del modelo
        return self.model.predict_future_progress(habit_name)
    
    def get_user_level_info(self):
        """Obtiene la información del nivel del usuario."""
        total_points, error = self.model.get_total_points()
        if error:
            return None, None, None, error

        level = self.model.get_user_level(total_points)
        next_level_points = self.model.get_next_level_points(level)

        if next_level_points is not None:
            points_needed = next_level_points - total_points
        else:
            points_needed = None

        return total_points, level, points_needed, None
    
    def mark_first_time(self, habit_list, view):
        """Marca un hábito como completado por primera vez."""
        # Obtener el hábito seleccionado de la lista
        habit_name = view.get_selected_habit(habit_list)
        if not habit_name:
            view.show_error_message("No hay ningún hábito seleccionado.")
            return

        # Obtener información del hábito desde el modelo
        habit_data, error = self.model.get_habit_data(habit_name)
        if error:
            view.show_error_message(error)
            return

        if habit_data is None:
            view.show_error_message(f"No se encontró el hábito: {habit_name}")
            return

        # Actualizar el estado del hábito en el modelo
        habit_id = habit_data[0]
        error = self.model.mark_first_done(habit_id)
        if error:
            view.show_error_message(error)
        else:
            view.show_habit_marked_message(habit_name)


        # Actualizar el estado del hábito
        habit_id = habit_data[0]
        error = self.model.mark_first_done(habit_id)
        if error:
            view.show_error_message(error)
        else:
            view.show_habit_marked_message(habit_name)

    def setup_notifications(self):
        """Configurar notificaciones automáticas."""
        self.timer = QTimer()
        self.timer.timeout.connect(self.send_notification)
        self.timer.start(360000) 

    def send_notification(self):
        """Llama a la vista para mostrar una notificación."""
        self.view.show_notification("¡No olvides completar tus hábitos de hoy!")

    def show_motivational_message(self):
        """Obtiene un mensaje del modelo y lo muestra a través de la vista."""
        message = self.model.get_random_message()
        self.view.display_message(message)