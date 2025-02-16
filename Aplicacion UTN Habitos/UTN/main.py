import sys
from views import HabitView
from observers import ConsoleObserver, GUIObserver , LogObserver
from models import HabitModel
from controllers import HabitController
from PyQt5.QtWidgets import QApplication
#from logg import iniciar_cliente_externo
# Configuración de PostgreSQL
DB_CONFIG = {
    "dbname": "habit_tracker",
    "user": "postgres",
    "password": "postgres",
    "host": "localhost",
    "port": "5432"
}

if __name__ == "__main__":
    app = QApplication(sys.argv)

    model = HabitModel(DB_CONFIG)
    model.initialize_db()



    controller = HabitController(model)

    view = HabitView(controller)
    

    # Agrega observadores
    log_observer = LogObserver()  #
    console_observer = ConsoleObserver()
    gui_observer = GUIObserver(view)
    model.agregar(log_observer)
    model.agregar(console_observer)
    model.agregar(gui_observer)
    #model.attach(HabitObserver("Progreso"))
    #model.attach(HabitObserver("Notificaciones"))

    
    

    view.show()
    sys.exit(app.exec_())

    sys.exit(app.exec_())

