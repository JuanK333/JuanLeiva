import socket
import logging
import uuid

def send_data(message, host="localhost", port=5001):
    try:
        client_id = str(uuid.uuid4())[:8]
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((host, port))
        client_socket.sendall(message.encode("utf-8"))
        client_socket.close()
        logging.info(f"{client_id} Mensaje enviado: {message}")  # Log de actividad en el cliente
        print(f"Mensaje enviado: {message}")
    except ConnectionRefusedError:
        print("Error: No se pudo conectar al servidor. Asegúrate de que está en ejecución.")
