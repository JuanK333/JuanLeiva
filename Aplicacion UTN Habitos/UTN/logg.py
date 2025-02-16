import socket
import logging
import time
import threading
from PyQt5.QtWidgets import QApplication, QPushButton, QVBoxLayout, QWidget, QLineEdit, QTextEdit
from PyQt5.QtCore import pyqtSignal, QThread

# Configurar logging para escribir en server.log
logging.basicConfig(filename="server.log", level=logging.INFO,
                    format="%(asctime)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")



class ServerThread(QThread):
    message_received = pyqtSignal(str)

    def __init__(self, host="localhost", port=5001, parent=None):
        super().__init__(parent)
        self.host = host
        self.port = port
        self.running = True
        self.parent_view = parent  # Guardamos la referencia a Views

    def run(self):
        try:
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.bind((self.host, self.port))
            server_socket.listen(5)
            print(f"Servidor escuchando en {self.host}:{self.port}")

            while self.running:
                client_socket, addr = server_socket.accept()
                data = client_socket.recv(1024).decode("utf-8")
                if data:
                    log_message = f"Mensaje recibido de {addr}: {data}"
                    print(log_message)

                    # Guardar en server.log
                    if self.parent_view:
                        self.parent_view.log_activity(log_message)

                    # Emitir señal para actualizar la UI
                    self.message_received.emit(log_message)
                client_socket.close()
        except Exception as e:
            print(f"Error en el servidor: {e}")

    def stop(self):
        self.running = False
        self.quit()


# -----------------------------------------------------------------------------------

#### **Clase `LogReaderThread` (Lectura en tiempo real de `server.log`)**
class LogReaderThread(QThread):
    log_update_signal = pyqtSignal(str)

    def run(self):
        """Lee los logs en tiempo real y los muestra en la UI."""
        try:
            with open("server.log", "r") as log_file:
                log_file.seek(0, 2)  # Moverse al final del archivo

                while True:
                    line = log_file.readline()
                    if line:
                        self.log_update_signal.emit(line.strip())
        except Exception as e:
            print(f"Error leyendo server.log: {e}")
