import time


def validate_arguments(arg_types=None):
    """Valida que los argumentos coincidan con los tipos esperados"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            if arg_types:
                args_to_validate = args[1:]  # Ignoramos self
                for i, (arg, expected_type) in enumerate(zip(args_to_validate, arg_types)):
                    if expected_type == str and func.__name__ == "add_habit":
                        # Validación específica para add_habit
                        if not arg.isalpha():
                            raise ValueError(
                                f"El nombre del hábito debe contener solo letras, recibido: '{arg}'"
                            )
                    if not isinstance(arg, expected_type):
                        raise ValueError(
                            f"Argumento {i + 1} de {func.__name__} debe ser {expected_type.__name__}, "
                            f"pero es {type(arg).__name__} con valor '{arg}'"
                        )
            return func(*args, **kwargs)
        return wrapper
    return decorator

class Controller:
    @validate_arguments(arg_types=[str])
    def add_habit(self, habit_name):
        self.model.add_habit(habit_name)


def retry(retries=3, delay=1):
    """Reintenta la ejecucion del metodo si ocurre un error"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    print(f"Error en {func.__name__}: {e}. Reintentando ({attempt + 1}/{retries})...")
                    time.sleep(delay)
            print(f"Error permanente en {func.__name__}. No se pudo completar después de {retries} intentos.")
            raise last_exception
        return wrapper
    return decorator

def measure_time(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"El método {func.__name__} tardó {end_time - start_time:.4f} segundos")
        return result
    return wrapper