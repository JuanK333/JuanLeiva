from PyQt5.QtWidgets import QMessageBox
from datetime import datetime


# Clase base para el patrón Observador
class Tema:
    def __init__(self):
        self.observadores = []

    def agregar(self, observador):
        self.observadores.append(observador)

    def quitar(self, observador):
        self.observadores.remove(observador)

    def notificar(self, mensaje):
        for observador in self.observadores:
            observador.update(mensaje)


class Observador:
    def update(self, mensaje):
        raise NotImplementedError("Este método debe ser implementado.")

class ConsoleObserver(Observador):
    def update(self, mensaje):
        print(f"Notificación recibida: {mensaje}")

class GUIObserver(Observador):
    def __init__(self, vista):
        self.vista = vista

    def update(self, mensaje):
        # Muestra el mensaje en la GUI usando un cuadro de diálogo
        QMessageBox.information(None, "Notificación", mensaje)


class LogObserver(Observador):
    def __init__(self, log_file="events.log"):
        self.log_file = log_file

    def update(self, mensaje):
        # Escribir el mensaje en un archivo de log
        with open(self.log_file, "a") as f:
            f.write(f"{datetime.now()} - {mensaje}\n")