# Se importan las librerías necesarias.
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from datetime import date

# Función de carga y chequeo de consistencia.
##Se crea una función que permite cargar todos los archivos necesarios del sistema de Alta/Baja de usuarios y trabajadores de un sistema ficticio de streaming de películas y realizar un chequeo de
##consistencia entre la información de los DataFrames, eliminando cualquier inconsistencia que se detecte.

def load_all(file_personas, file_trabajadores, file_usuarios, file_peliculas, file_scores):
    # Se cargan las bases de datos.
    df_personas = pd.read_csv(file_personas)
    df_trabajadores = pd.read_csv(file_trabajadores)
    df_usuarios = pd.read_csv(file_usuarios)
    df_peliculas = pd.read_csv(file_peliculas)
    df_scores = pd.read_csv(file_scores)

    # Se arreglan las bases: eliminan filas con Nan/Null, se homogeniza nombre de variables, cambia formato de campos fecha,
    # homogenizado a %d-%m-%a (salvo fecha de nacimiento que solo se tiene año) y elimina campos extras.
    ## df_personas
    df_personas = df_personas.dropna()
    df_personas = df_personas.rename(columns = {'Full Name':'full_name', 'year of birth':'year_birth',
                                           'Zip Code':'zip_code', 'id':'id_persona', 'Gender':'gender'})
    df_personas['year_birth'] = pd.to_numeric(df_personas['year_birth'])

    ## df_trabajadores
    df_trabajadores = df_trabajadores.dropna()
    df_trabajadores = df_trabajadores.rename(columns = {'Working Hours':'time_range', 'Start Date':'join_date', 'id': 'id_persona',
                                                        'Category':'category', 'Position':'position'})
    df_trabajadores['join_date'] = pd.to_datetime(df_trabajadores['join_date'])
    df_trabajadores['join_date'] = df_trabajadores['join_date'].dt.strftime('%d-%m-%Y')

    ## df_usuarios
    df_usuarios = df_usuarios.dropna()
    df_usuarios = df_usuarios.rename(columns = {'Active Since':'start_date', 'Occupation': 'occupation', 'id': 'id_persona'})
    df_usuarios['start_date'] = pd.to_datetime(df_usuarios['start_date'])
    df_usuarios['start_date'] = df_usuarios['start_date'].dt.strftime('%d-%m-%Y')

    ## df_películas
    df_peliculas = df_peliculas.dropna()
    df_peliculas=df_peliculas.rename(columns = {'Name':'name', 'Release Date':'release_date', 'id':'id_movie', 'IMDB URL':'url'})
    df_peliculas['release_date'] = pd.to_datetime(df_peliculas['release_date'])
    df_peliculas['release_date'] = df_peliculas['release_date'].dt.strftime('%d-%m-%Y')
    ### Se crea un campo que indica el/los géneros correspondientes a esa película.
    df_peliculas['gender_movie'] = df_peliculas.apply(lambda x: ', '.join([col for col, val in x.items() if val == 1]), axis=1)

    ## df_scores
    df_scores = df_scores.dropna()
    df_scores = df_scores.rename(columns = {'Unnamed: 0': 'id', 'Date':'stamp_date', 'user_id': 'id_persona', 'movie_id':'id_movie'})
    df_scores['stamp_date'] = pd.to_datetime(df_scores['stamp_date'])
    df_scores['stamp_date'] = df_scores['stamp_date'].dt.strftime('%d-%m-%Y')

    # Se chequea la consistencia entre DF (4 pruebas)
    ## Se verifica que los IDs de usuarios estén presentes en el df de personas y devuelve un mensaje.
    usuarios_no_en_personas = df_usuarios[~df_usuarios['id_persona'].isin(df_personas['id_persona'])]
    if not usuarios_no_en_personas.empty:
        df_usuarios = df_usuarios[~df_usuarios['id_persona'].isin(usuarios_no_en_personas['id_persona'])]
        consist1 = print("Se encontraron usuarios que no están en el DataFrame de personas. Se eliminan los mismos.")
    else:
        consist1 =print("No se encontraron usuarios que no estén en el DataFrame de personas.")

    ## Se verifica que los IDs de trabajadores estén presentes en el df de personas y devuelve un mensaje.
    trabajadores_no_en_personas = df_trabajadores[~df_trabajadores['id_persona'].isin(df_personas['id_persona'])]
    if not trabajadores_no_en_personas.empty:
        df_trabajadores = df_trabajadores[~df_trabajadores['id_persona'].isin(trabajadores_no_en_personas['id_persona'])]
        consist2 = print("Se encontraron trabajadores que no están en el DataFrame de personas. Se eliminan los mismos.")
    else:
        consist2 =print("No se encontraron trabajadores que no estén en el DataFrame de personas.")

    ## Se verifica que los IDs de pelìculos del df de scores entén presentes en el df de películas y devuelve un mensaje.
    scores_no_en_peliculas = df_scores[~df_scores['id_movie'].isin(df_peliculas['id_movie'])]
    if not scores_no_en_peliculas.empty:
        df_scores = df_scores[~df_scores['id_movie'].isin(scores_no_en_peliculas['id_movie'])]
        consist3 = print("Se encontraron scores de películas que no están en el DataFrame de películas. Se eliminan los mismos.")
    else:
        consist3 =print("No se encontraron scores de películas que no estén en el DataFrame de películas.")

    ## Se verifica que los IDs de usuarios del df de scores estén presentes en el df de usuarios y devuelve un mensaje.
    scores_no_en_usuarios = df_scores[~df_scores['id_persona'].isin(df_usuarios['id_persona'])]
    if not scores_no_en_usuarios.empty:
        df_scores = df_scores[~df_scores['id_persona'].isin(scores_no_en_peliculas['id_persona'])]
        consist4= print("Se encontraron usuarios que calificaron películas que no están en el DataFrame de películas. Se eliminan los mismos.")
    else:
        consist4 =print("No se encontraron usuarios que calificaran películas que no estén en el DataFrame de películas.")

    return df_personas, df_trabajadores, df_usuarios, df_peliculas, df_scores


df_personas, df_trabajadores, df_usuarios, df_peliculas, df_scores = load_all(
    'personas.csv',
    'trabajadores.csv',
    'usuarios.csv',
    'peliculas.csv',
    'scores.csv')
# Función de salvado.
# Se crea una función que permite guardar/salvar los 5 archivos resultantes de la carga y los controles, y avisa si no se puede guardar alguno.
def save_all(df_personas, df_trabajadores, df_usuarios, df_peliculas, df_scores,
             file_personas="personas2.csv", file_trabajadores="trabajadores2.csv", file_usuarios="usuarios2.csv",
             file_peliculas="peliculas2.csv", file_scores="scores2.csv"):
    try:
        df_personas.to_csv(file_personas, index=False)
        df_trabajadores.to_csv(file_trabajadores, index=False)
        df_usuarios.to_csv(file_usuarios, index=False)
        df_peliculas.to_csv(file_peliculas, index=False)
        df_scores.to_csv(file_scores, index=False)
        print("Archivos guardados exitosamente.")
        return 0
    except Exception as e:
        print(f"Error al guardar los archivos: {str(e)}")
        return -1

save_all(df_personas, df_trabajadores, df_usuarios, df_peliculas, df_scores,
             file_personas="personas2.csv", file_trabajadores="trabajadores2.csv", file_usuarios="usuarios2.csv",
             file_peliculas="peliculas2.csv", file_scores="scores2.csv")

# Definición de las clases.
## Se define la clase GESTIONPERSONAS que permite dar de alta/baja personas, consultar infomación y obtener estadísticas.
class GestionPersonas:
    def __init__(self, id_persona, full_name, year_birth, gender, zip_code):
        self.id_persona = id_persona
        self.full_name = full_name
        self.year_birth = year_birth
        self.gender = gender
        self.zip_code = zip_code


## Método para imprimir la información de una persona.
    def __repr__(self):
        return f"GestionPersonas(id_persona='{self.id_persona}', full_name='{self.full_name}', year_birth='{self.year_birth}', gender='{self.gender}', zip_code='{self.zip_code}' )"


## Método para cargar el DF la a partir de un archivo csv.
### Recibe el nombre del archivo csv, valida su estructura y devuelve un df con la información cargada del archivo 'filename'. Si no se encuentra el archivo, devuleve un mensaje de error.
    @classmethod
    def create_df_from_csv(self, filename):
        try:
            df_us = pd.read_csv(filename)
            return df_us
        except FileNotFoundError:
            print("ERROR: El archivo CSV especificado no se encontró.")
            return None


## Método para dar de alta una persona, agregándola en el df.
### Si el id no se encuentra, toma el id más alto del df y le suma uno. Si el id ya existe, no la agrega y devuelve un mensaje de error.
    def write_df(self, df):
        if self.id_persona in df['id_persona']:
            print("ERROR: El ID de la persona ya existe en el DataFrame.")
            df_actualizada = df
        else:
            self.id_persona= df['id_persona'].max() + 1
            df_nuevapersona = pd.DataFrame([self.__dict__])
            df_actualizada = pd.concat([df, df_nuevapersona], ignore_index=True)
        return df_actualizada


## Método para filtrar el DF por una o más característica/atributo.
### Devuelve un mensaje de error si no encuentra personas que cumplan con los criterios establecidos.
    @classmethod
    def get_from_df(cls, df, id_persona=None, full_name=None, year_birth=[None, None], gender=None, zip_code=None):
        convered_df = df.copy()
        convered_df['year_birth'] = convered_df['year_birth'].astype(int)
        query = {}
        if id_persona:
            query['id_persona'] = id_persona
        if full_name:
            query['full_name'] = full_name
        if year_birth:
            query['year_birth'] = list(range(year_birth[0], year_birth[1]+1))
        if gender:
            query['gender'] = gender
        if zip_code:
            query['zip_code'] = zip_code
        result = convered_df.query(' & '.join([f'{k} == "{v}"' if isinstance(v, str) else f'{k} == {v}' for k, v in query.items()]))
        if result.empty:
            print("ERROR: No se encontraron personas que cumplan con los criterios de búsqueda.")
        return result


## Método para imprimir una serie de estadísticas calculadas y gráficos a partir de los resultados de una consulta a el df.
### Devuelve un mensaje de error si no encuentra personas que cumplan con los criterios establecidos.
    @classmethod
    def get_stats(cls, df, year_birth=[None, None],  gender=None):
        filtered_df = df.copy()
        filtered_df['year_birth'] = filtered_df['year_birth'].astype(int)
        filtered_df = filtered_df[filtered_df['year_birth'].between(year_birth[0], year_birth[1])]
        if gender:
            filtered_df = filtered_df[filtered_df['gender'].isin(gender)]
        if filtered_df.empty:
            print("ERROR: No se encontraron personas que cumplan con los criterios de búsqueda.")
            return

    # Cantidad total de personas
        total_personas = filtered_df.shape[0]
        print(f"Cantidad total de personas: {total_personas}")

    # Edad promedio de las personas
        edad_promedio = sum(date.today().year-filtered_df['year_birth'])/total_personas
        print(f"Edad promedio de las personas: {round(edad_promedio)}")

    # Gráfico de barras: cantidad de personas por año de nacimiento en la ventana de tiempo señalada
        plt.figure(figsize=(12, 6))
        plt.subplot(1, 2, 1)
        years = filtered_df['year_birth'].value_counts().index
        count_per = filtered_df['year_birth'].value_counts().values
        plt.bar(years, count_per, color ='lightcoral', width = 0.4)
        plt.title("Cantidad de personas por año de nacimiento", fontweight='bold')
        plt.xlabel("Año de nacimiento")
        plt.ylabel("Cantidad")
        plt.xticks(years, rotation=90)
        plt.grid(axis='y')

    # Gráfico de barras: cantidad de personas por género en la ventana de tiempo señalada
        plt.subplot(1, 2, 2)
        generos = filtered_df['gender'].value_counts().index
        count_gen = filtered_df['gender'].value_counts().values
        plt.bar(generos, count_gen, color = 'lightblue', width = 0.8)
        plt.title("Cantidad de personas por género", fontweight='bold')
        plt.xlabel("Género")
        plt.ylabel("Cantidad")
        plt.xticks(generos)
        plt.grid(axis='y')

        plt.tight_layout()
        plt.show()


## Método para dar de baja una persona, borrándola de la base.
### Para realizar el borrado, todas las características/atributos de la misma deben coincidir con lo existente en la base. Caso contrario imprime un mensaje de error.
    def remove_from_df(self, df):
        match = df.query('id_persona == @self.id_persona and full_name == @self.full_name and year_birth == @self.year_birth and gender == @self.gender and zip_code == @self.zip_code').index
        if len(match) == 0:
            print("ERROR: No se encontró la persona en el DataFrame.")
        else:
            df = df.drop(match)
            print("Persona eliminada de la base.")
        return df

## Se define la clase GESTIONUSUARIOS que permite dar de alta/baja personas, consultar infomación y obtener estadísticas.
class GestionUsuarios(GestionPersonas):
    def __init__(self, id_persona, occupation, start_date):
        super().__init__(id_persona, full_name=None, year_birth=None, gender=None, zip_code=None)
        self.occupation = occupation
        self.start_date = start_date


## Método para imprimir la información de una persona.
    def __repr__(self):
        return f"GestionUsuarios(id_persona='{self.id_persona}', occupation='{self.occupation}', start_date='{self.start_date}')"


## Método para cargar el DF la a partir de un archivo csv.
### Recibe el nombre del archivo csv, valida su estructura y devuelve un df con la información cargada del archivo 'filename'. Si no se encuentra el archivo, devuleve un mensaje de error.
    @classmethod
    def create_df_from_csv(self, filename):
        try:
            df_us = pd.read_csv(filename)
            return df_us
        except FileNotFoundError:
            print("ERROR: El archivo CSV especificado no se encontró.")
            return None


## Método para dar de alta un usuario, agregándola en el df.
### Si el id no se encuentra, toma el id más alto del df y le suma uno. Si el id ya existe, no la agrega y devuelve un mensaje de error.
    def write_df(self, df):
        if self.id_persona in df['id_persona']:
            print("ERROR: El ID del usuario ya existe en el DataFrame.")
            df_actualizada = df
        else:
            self.id_persona = df['id_persona'].max() + 1
            df_nuevousuario = pd.DataFrame([self.__dict__])
            df_actualizada = pd.concat([df, df_nuevousuario], ignore_index=True)
            df_actualizada = df_actualizada.drop(columns=['full_name', 'year_birth', 'gender', 'zip_code'] )
        return df_actualizada


## Método para filtrar el DF por una o más característica/atributo.
### Devuelve un mensaje de error si no encuentra personas que cumplan con los criterios establecidos.
    @classmethod
    def get_from_df(cls, df, id_persona=None, occupation=None, start_date=[None, None]):
        convert_df = df.copy()
        convert_df['start_date'] = pd.to_datetime(convert_df['start_date'], format='%d-%m-%Y').dt.year
        query = {}
        if id_persona:
            query['id_persona'] = id_persona
        if occupation:
            query['occupation'] = occupation
        if start_date:
            query['start_date'] = list(range(start_date[0], start_date[1]+1))
        result = convert_df.query(' & '.join([f'{k} == "{v}"' if isinstance(v, str) else f'{k} == {v}' for k, v in query.items()]))
        if result.empty:
            print("ERROR: No se encontraron usuarios que cumplan con los criterios de búsqueda.")
        return result


## Método para imprimir una serie de estadísticas calculadas y gráficos a partir de los resultados de una consulta a el df.
### Devuelve un mensaje de error si no encuentra personas que cumplan con los criterios establecidos.
    @classmethod
    def get_stats(cls, df, occupation=None, start_date=[None, None]):
        filtered_df = df.copy()
        filtered_df['start_date'] = pd.to_datetime(filtered_df['start_date'], format='%d-%m-%Y').dt.year
        filtered_df = filtered_df[filtered_df['start_date'].between(start_date[0], start_date[1])]
        if occupation:
            filtered_df = filtered_df[filtered_df['occupation'].isin(occupation)]
        if filtered_df.empty:
            print("ERROR: No se encontraron usuarios que cumplan con los criterios de búsqueda.")
            return

    # Cantidad total de usuarios
        total_usuarios = filtered_df.shape[0]
        print(f"Cantidad total de usuarios: {total_usuarios}")

    # Antiguedad promedio de los usuarios
        antig_promedio = (date.today().year-filtered_df['start_date']).mean()
        print(f"Antiguedad promedio de los usuarios: {round(antig_promedio)}")

    # Gráfico de barras: cantidad de usuarios por año dados de alta en la ventana de tiempo señalada
        plt.figure(figsize=(12, 6))
        plt.subplot(1, 2, 1)
        years = filtered_df['start_date'].value_counts().index
        count_usu = filtered_df['start_date'].value_counts().values
        plt.bar(years, count_usu, color ='lightcoral', width = 0.4)
        plt.title("Cantidad de usuarios por año de alta", fontweight='bold')
        plt.xlabel("Año de alta")
        plt.ylabel("Cantidad")
        plt.xticks(years, rotation=90)
        plt.grid(axis='y')

    # Gráfico de barras: cantidad de usuarios por ocupación en la ventana de tiempo señalada
        plt.subplot(1, 2, 2)
        occupations = filtered_df['occupation'].value_counts().index
        count_ocu = filtered_df['occupation'].value_counts().values
        plt.bar(occupations, count_ocu, color = 'lightblue', width = 0.8)
        plt.title("Cantidad de usuarios por ocupación",fontweight='bold')
        plt.xlabel("Ocupación")
        plt.ylabel("Cantidad")
        plt.xticks(occupations, rotation=90)
        plt.grid(axis='y')

        plt.tight_layout()
        plt.show()


## Método para dar de baja un usuario, borrándola de la base.
### Para realizar el borrado, todas las características/atributos de la misma deben coincidir con lo existente en la base. Caso contrario imprime un mensaje de error.
    def remove_from_df(self, df):
        match = df.query('id_persona == @self.id_persona and start_date == @self.start_date and occupation == @self.occupation').index
        if len(match) == 0:
            print("ERROR: No se encontró el usuario en el DataFrame.")
        else:
            df = df.drop(match)
            print("Usuario eliminado del DateFrame.")
        return df

## Se define la clase GESTIONTRABAJADORES que permite dar de alta/baja personas, consultar infomación y obtener estadísticas.
class GestionTrabajadores(GestionPersonas):
    def __init__(self, id_persona, position, category, time_range, join_date):
        super().__init__(id_persona, full_name=None, year_birth=None, gender=None, zip_code=None)
        self.position = position
        self.category = category
        self.time_range = time_range
        self.join_date = join_date


## Método para imprimir la información de una persona.
    def __repr__(self):
        return f"GestionTrabajadores(id_persona='{self.id_persona}', position='{self.position}', category='{self.category}', time_range='{self.time_range}, join_date='{self.join_date}')"


## Método para cargar el DF la a partir de un archivo csv.
### Recibe el nombre del archivo csv, valida su estructura y devuelve un df con la información cargada del archivo 'filename'. Si no se encuentra el archivo, devuleve un mensaje de error.
    @classmethod
    def create_df_from_csv(self, filename):
        try:
            df_us = pd.read_csv(filename)
            return df_us
        except FileNotFoundError:
            print("ERROR: El archivo CSV especificado no se encontró.")
            return None


## Método para dar de alta un usuario, agregándola en el df.
### Si el id no se encuentra, toma el id más alto del df y le suma uno. Si el id ya existe, no la agrega y devuelve un mensaje de error.
    def write_df(self, df):
        if self.id_persona in df['id_persona']:
            print("ERROR: El ID del trabajador ya existe en el DataFrame.")
            df_actualizada = df
        else:
            self.id_persona = df['id_persona'].max() + 1
            df_nuevotrabajador = pd.DataFrame([self.__dict__])
            df_actualizada = pd.concat([df, df_nuevotrabajador], ignore_index=True)
            df_actualizada = df_actualizada.drop(columns=['full_name',  'year_birth', 'gender', 'zip_code'] )
        return df_actualizada


## Método para filtrar el DF por una o más característica/atributo.
### Devuelve un mensaje de error si no encuentra personas que cumplan con los criterios establecidos.
    @classmethod
    def get_from_df(cls, df, id_persona=None, position=None, category=None, join_date=[None, None]):
        convert_df = df.copy()
        convert_df['join_date'] = pd.to_datetime(convert_df['join_date'], format='%d-%m-%Y').dt.year
        query = {}
        if id_persona:
            query['id_persona'] = id_persona
        if position:
            query['position'] = position
        if category:
            query['category'] = category
        if join_date:
            query['join_date'] = list(range(join_date[0], join_date[1]+1))
        result = convert_df.query(' & '.join([f'{k} == "{v}"' if isinstance(v, str) else f'{k} == {v}' for k, v in query.items()]))
        if result.empty:
            print("ERROR: No se encontraron trabajadores que cumplan con los criterios de búsqueda.")
        return result


## Método para imprimir una serie de estadísticas calculadas y gráficos a partir de los resultados de una consulta a el df.
### Devuelve un mensaje de error si no encuentra personas que cumplan con los criterios establecidos.
    @classmethod
    def get_stats(cls, df, position=None, category=None, join_date=[None, None]):
        filtered_df = df.copy()
        filtered_df['join_date'] = pd.to_datetime(filtered_df['join_date'], format='%d-%m-%Y').dt.year
        filtered_df = filtered_df[filtered_df['join_date'].between(join_date[0], join_date[1])]
        if position:
            filtered_df = filtered_df[filtered_df['position'].isin(position)]
        if category:
            filtered_df = filtered_df[filtered_df['category'].isin(category)]
        if filtered_df.empty:
            print("ERROR: No se encontraron trabajadores que cumplan con los criterios de búsqueda.")
            return

    # Cantidad total de trabajadores
        total_trabajadores = filtered_df.shape[0]
        print(f"Cantidad total de trabajadores: {total_trabajadores}")

    # Antiguedad promedio de los trabajadores
        antig_promedio = sum(date.today().year-filtered_df['join_date'])/total_trabajadores
        print(f"Antiguedad promedio de los trabajadores: {round(antig_promedio)}")

    # Gráfico de barras: cantidad de trabajadores por año dados de alta en la ventana de tiempo señalada
        plt.figure(figsize=(12, 6))
        plt.subplot(1, 2, 1)
        years = filtered_df['join_date'].value_counts().index
        count_tra = filtered_df['join_date'].value_counts().values
        plt.bar(years, count_tra, color ='lightcoral', width = 0.4)
        plt.title("Cantidad de trabajadores por año de alta", fontweight='bold')
        plt.xlabel("Año de alta")
        plt.ylabel("Cantidad")
        plt.xticks(years, rotation=90)
        plt.grid(axis='y')

    # Gráfico de barras: cantidad de trabajadores por categoría en la ventana de tiempo señalada
        plt.subplot(1, 2, 2)
        categories = filtered_df['category'].value_counts().index
        count_cat = filtered_df['category'].value_counts().values
        plt.bar(categories, count_cat, color = 'lightblue', width = 0.8)
        plt.title("Cantidad de trabajadores por categoría", fontweight='bold')
        plt.xlabel("Categoría")
        plt.ylabel("Cantidad")
        plt.xticks(categories)
        plt.grid(axis='y')

        plt.tight_layout()
        plt.show()


## Método para dar de baja un trabajador, borrándola de la base.
### Para realizar el borrado, todas las características/atributos de la misma deben coincidir con lo existente en la base. Caso contrario imprime un mensaje de error.
    def remove_from_df(self, df):
        match = df.query('id_persona == @self.id_persona and position == @self.position and category == @self.category and time_range == @self.time_range and join_date == @self.join_date').index
        if len(match) == 0:
            print("ERROR: No se encontró el trabajador en el DataFrame.")
        else:
            df = df.drop(match)
            print("Trabajador eliminado del DateFrame.")
        return df

## Se define la clase GESTIONPELICULAS que permite dar de alta/baja películas, consultar infomación y obtener estadísticas.
class GestionPeliculas:
    campos_genero = ['unknown', 'Action', 'Adventure', 'Animation', 'Children\'s', 'Comedy',
        'Crime', 'Documentary', 'Drama', 'Fantasy', 'Film-Noir',
        'Horror', 'Musical', 'Mystery', 'Romance', 'Sci-Fi',
        'Thriller', 'War', 'Western']

    def __init__(self, id_movie, name, release_date, url, gender_movie, **kwargs):
        self.id_movie = id_movie
        self.name = name
        self.release_date = release_date
        self.url = url
        self.gender_movie = gender_movie

        # Se inicializa con 0 los campos correspondientes a género.
        for gender in self.campos_genero:
            setattr(self, gender, 0)


## Método para imprimir la información de una película.
    def __repr__(self):
        return f"GestionPeliculas(id_movie='{self.id_movie}', name='{self.name}', release_date='{self.release_date}', url = {'url'}, gender_movie='{self.gender_movie}' )"


## Método para cargar el DF a partir de un archivo csv.
### Recibe el nombre del archivo csv, valida su estructura y devuelve un DF con la información cargada del archivo 'filename'. Si no se encuentra el archivo, devuleve un mensaje de error.
    @classmethod
    def create_df_from_csv(self, filename):
        try:
            df_us = pd.read_csv(filename)
            return df_us
        except FileNotFoundError:
            print("ERROR: El archivo CSV especificado no se encontró.")
            return None


## Método para dar de alta una película, agregándola en el df.
### Si el id no se encuentra, toma el id más alto del df y le suma uno. Si id ya existe, no la agrega y devuelve un mensaje de error.
    def write_df(self, df):
        if self.id_movie in df['id_movie']:
            print("ERROR: El ID de la película ya existe en el DataFrame.")
            df_actualizada = df
        else:
            self.id_movie = df['id_movie'].max() + 1 if not df.empty else 1
            df_nuevapelicula = pd.DataFrame([self.__dict__])

    ## Se marcan los géneros informados con 1 y los no informados con 0.
            for gender in self.gender_movie.split(','):
                if gender in self.campos_genero:
                    df_nuevapelicula[gender] = 1

            for gender in self.campos_genero:
                if gender not in df.columns:
                    df_nuevapelicula[gender] = 0

            df_actualizada = pd.concat([df, df_nuevapelicula], ignore_index=True)
            return df_actualizada


## Método para filtrar la base por determinada característica/atributo.
### Devuelve un mensaje de error si no encuentra películas que cumplan con los criterios establecidos.
    @classmethod
    def get_from_df(cls, df, id_movie=None, name=None, release_date=[None, None], gender_movie=None):
        convert_df = df.copy()
        convert_df['release_date'] = pd.to_datetime(convert_df['release_date'], format='%d-%m-%Y').dt.year
        query = {}
        if id_movie:
            query['id_movie'] = id_movie
        if name:
            query['name'] = name
        if release_date:
            query['release_date'] = list(range(release_date[0], release_date[1]+1))
        if gender_movie:
            query['gender_movie'] = gender_movie
        result = convert_df.query(' & '.join([f'{k} == "{v}"' if isinstance(v, str) else f'{k} == {v}' for k, v in query.items()]))
        if result.empty:
            print("ERROR: No se encontraron películas que cumplan con los criterios de búsqueda.")
        return result


## Método para imprimir una serie de estadísticas calculadas y gráficos a partir de los resultados de una consulta a el df.
### Devuelve un mensaje de error si no encuentra películas que cumplan con los criterios establecidos.
    @classmethod
    def get_stats(cls, df, release_date=[None, None], gender_movie=None):
        filtered_df = df.copy()
        filtered_df['release_date'] = pd.to_datetime(filtered_df['release_date'], format='%d-%m-%Y').dt.year
        filtered_df = filtered_df[filtered_df['release_date'].between(release_date[0], release_date[1])]

        if gender_movie:
            # Se separan los géneros especificados y eliminan espacios adicionales
            gender_list = [g.strip() for g in gender_movie.split(',')]
            # Se verifica la existencia de cada género en los campos del DF, devolviendo error si ninguno existe
            valid_gender = [gender for gender in gender_list if gender in cls.campos_genero]
            if not valid_gender:
                print("ERROR: Género/s proporcionado/s inexitente/s.")
                return
            # Se crea un campo adicional para películas que tienen más de un género
            if len(valid_gender) > 1:
                many_gender_column = '_AND_'.join(valid_gender)
                filtered_df[many_gender_column] = filtered_df[valid_gender].sum(axis=1) == len(valid_gender)
                valid_gender.append(many_gender_column)
            # Se filtran los resgistros que contienen al menos uno de los géneros especificados y se cuentan
                filtered_df = filtered_df[(filtered_df[valid_gender[:-1]].sum(axis=1) > 0)]
            else:
                filtered_df = filtered_df[(filtered_df[valid_gender].sum(axis=1) > 0)]
            genero_counts = filtered_df[valid_gender].sum() if not filtered_df.empty else pd.Series()
        else:
            genero_counts = filtered_df[cls.campos_genero].sum()

        if filtered_df.empty:
            print("ERROR: No se encontraron películas que cumplan con los criterios de búsqueda.")
            return

        if not genero_counts.empty:
        # Cantidad total de películas
            total_películas = filtered_df.shape[0]
            print(f"Cantidad total de películas: {total_películas}")

        # Película más vieja y más nueva
            oldest_movie = filtered_df.loc[filtered_df['release_date'].idxmin(), 'name']
            newest_movie = filtered_df.loc[filtered_df['release_date'].idxmax(), 'name']
            print("\nPelícula más vieja:")
            print(oldest_movie)
            print("\nPelícula más nueva:")
            print(newest_movie)

        # Gráfico de barras: cantidad de películas por año de lanzamiento en la ventana de tiempo señalada
            plt.figure(figsize=(12, 6))
            plt.subplot(1, 2, 1)
            years = filtered_df['release_date'].value_counts().index
            count_mov = filtered_df['release_date'].value_counts().values
            plt.bar(years, count_mov, color='lightcoral', width=0.4)
            plt.title("Cantidad de películas por año de lanzamiento", fontweight='bold')
            plt.xlabel("Año de lanzamiento")
            plt.ylabel("Cantidad")
            plt.xticks(years, rotation=90)
            plt.grid(axis='y')

        # Gráfico de barras: cantidad de películas por género en la ventana de tiempo señalada
            plt.subplot(1, 2, 2)
            plt.bar(genero_counts.index, genero_counts.values, color='lightblue', width=0.8)
            plt.title("Cantidad de películas por género", fontweight='bold')
            plt.xlabel("Género")
            plt.ylabel("Cantidad")
            plt.xticks(rotation=90)
            plt.grid(axis='y')

            plt.tight_layout()
            plt.show()

        else:
            print("ERROR: Género no existente en la base de datos.")


## Método para dar de baja una película, borrándola de la base.
### Para realizar el borrado, todas las características/atributos de la misma deben coincidir con lo existente en la base. Caso contrario imprime un mensaje de error.
    def remove_from_df(self, df):
        match = df.query('id_movie == @self.id_movie and name == @self.name and release_date == @self.release_date and gender_movie == @self.gender_movie').index #####VER
        if len(match) == 0:
            print("ERROR: No se encontró la película en DataFrame.")
        else:
            df = df.drop(match)
            print("Película eliminada de la base.")
        return df

## Se define la clase SCORES que permite dar de alta/baja películas, consultar infomación y obtener estadísticas.
class GestionScores:
    def __init__(self, id, id_persona, id_movie, rating, stamp_date):
        self.id = id
        self.id_persona = id_persona
        self.id_movie = id_movie
        self.rating = rating
        self.stamp_date = stamp_date


## Método para imprimir la información de un score.
    def __repr__(self):
        return f"GestionScores(id={self.id}, id_persona={self.id_persona}, id_movie='{self.id_movie}', rating='{self.rating}', stamp_date='{self.stamp_date}' )"


## Método para cargar el DF a partir de un archivo csv.
### Recibe el nombre del archivo csv, valida su estructura y devuelve un DF con la información cargada del archivo 'filename'. Si no se encuentra el archivo, devuleve un mensaje de error.
    @classmethod
    def create_df_from_csv(cls, filename):
        try:
            df_us = pd.read_csv(filename)
            return df_us
        except FileNotFoundError:
            print("El archivo CSV especificado no se encontró.")
            return None


## Método para dar de alta una película, agregándola en el df.
### Si el id no se encuentra, toma el id más alto del df y le suma uno. Si id ya existe, no la agrega y devuelve un mensaje de error.
    def write_df(self, df):
        if self.id in df['id']:
            print("ERROR: La película ya está calificada en el DataFrame.")
            df_actualizada = df
        else:
            self.id = df['id'].max() + 1
            df_nuevoscore = pd.DataFrame([self.__dict__])
            df_actualizada = pd.concat([df, df_nuevoscore], ignore_index=True)
        return df_actualizada


## Método para filtrar la base por determinada característica/atributo.
### Devuelve un mensaje de error si no encuentra películas que cumplan con los criterios establecidos.
    @classmethod
    def get_from_df(cls, df, id=None, id_persona=None, id_movie=None, rating=[None, None], stamp_date=[None, None]):
        convert_df = df.copy()
        convert_df['stamp_date'] = pd.to_datetime(convert_df['stamp_date'], format='%d-%m-%Y').dt.year
        convert_df['rating'] = convert_df['rating'].astype('int64')
        query = {}
        if id:
            query['id'] = id
        if id_persona:
            query['id_persona'] = id_persona
        if id_movie:
            query['id_movie'] = id_movie
        if rating:
            query['rating'] = list(range(rating[0], rating[1]+1))
        if stamp_date:
            query['stamp_date'] = list(range(stamp_date[0], stamp_date[1]+1))
        result = convert_df.query(' & '.join([f'{k} == "{v}"' if isinstance(v, str) else f'{k} == {v}' for k, v in query.items()]))

        if result.empty:
            print("ERROR: No se encontraron películas que cumplan con los criterios de búsqueda.")
        return result


## Método para imprimir una serie de estadísticas calculadas y gráficos a partir de los resultados de una consulta a el df.
### Devuelve un estadísticas generales o el score de una película indicada.
    @classmethod
    def get_stats(cls, df, dfp=df_personas, dfu=df_usuarios, dfm=df_peliculas, id_movie=None):
    # Se construye un base agregada que integra información de scores, personas, usuarios y películas)
        merged_data = pd.merge( df, dfp, how='right', left_on='id_persona', right_on='id_persona')
        merged_data = pd.merge(merged_data, dfu, left_on='id_persona', right_on='id_persona')
        merged_data = pd.merge(merged_data, dfm,left_on='id_movie',right_on='id_movie')

    # Se agrega un nuevo campo: edad de la persona.
        merged_data['release_date'] = pd.to_datetime(merged_data['release_date'], format='%d-%m-%Y').dt.year
        merged_data['edad'] = date.today().year - merged_data['year_birth']

        if not id_movie is None:
            score_filtrados = merged_data.loc[merged_data['id_movie'] == id_movie]
            average_scores_filtrados = round(score_filtrados['rating'].mean(),1)
            print("\nScore promedio de la película:", merged_data.loc[merged_data['id_movie'] == id_movie, 'name'].iloc[0])
            print(average_scores_filtrados)
        else:
            # Score promedio por año
            merged_data['stamp_date'] = pd.to_datetime(merged_data['stamp_date'], format='%d-%m-%Y').dt.year
            average_scores_by_year = merged_data.groupby('stamp_date')['rating'].mean()
            # Score promedio por género
            average_scores_by_gender = merged_data.groupby('gender')['rating'].mean()
            # Score promedio por edad
            average_scores_by_age = merged_data.groupby('edad')['rating'].mean()
            # Score promedio por ocupación
            average_scores_by_occupation = merged_data.groupby('occupation')['rating'].mean()

            print("\nScore promedio por año:")
            print(average_scores_by_year)
            print("\nScore premedio por género:")
            print(average_scores_by_gender)

            # Gráfico de barras: cantidad de películas por año de lanzamiento en la ventana de tiempo señalada
            plt.figure(figsize=(12, 6))
            plt.subplot(1, 2, 1)
            average_scores_by_age.plot(kind='bar', color='lightcoral')
            plt.title('Score promedio por edad', fontweight='bold')
            plt.xlabel('Edad')
            plt.ylabel('Score promedio')
            plt.xticks(rotation=90,fontsize=6)
            plt.grid(axis='y')

        # Gráfico de barras: cantidad de películas por género en la ventana de tiempo señalada
            plt.subplot(1, 2, 2)
            average_scores_by_occupation.plot(kind='bar', color='lightblue')
            plt.title('Score promedio por ocupación', fontweight='bold')
            plt.xlabel('Ocupación')
            plt.ylabel('Score promedio')
            plt.xticks(rotation=90)
            plt.grid(axis='y')

            plt.tight_layout()
            plt.show()


    ## Método para dar de baja un score, borrándola de la base.
    ### Para realizar el borrado, todas las características/atributos de la misma deben coincidir con lo existente en la base. Caso contrario imprime un mensaje de error.
    def remove_from_df(self, df):
        match = df.query('id == @self.id and id_persona == @self.id_persona and id_movie == @self.id_movie and rating == @self.rating and stamp_date == @self.stamp_date').index
        if len(match) == 0:
            print("ERROR: No se encontró el score en el DataFrame.")
        else:
            df = df.drop(match)
            print("Score eliminado del DataFrame.")
        return df
