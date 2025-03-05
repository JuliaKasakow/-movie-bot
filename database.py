import mysql.connector
import time
from utils import log_error

dbconfig_read = {
    'host': 'hostname',
    'user': 'user',
    'password': 'password',
    'database': 'sakila'
}

dbconfig_write = {
    'host': 'hostname',
    'user': 'user',
    'password': 'password',
    'database': 'ich_edit'
}


class Database:
    def __init__(self, config):
        self.config = config
        self.connection = None

    def connect(self):
        """Устанавливает соединение с базой данных, если оно не активно."""
        if self.connection is None or not self.connection.is_connected():
            self.connection = mysql.connector.connect(**self.config)

    def execute_query(self, query, params=None):
        """Выполняет SELECT-запрос и возвращает результат."""
        self.connect()
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute(query, params)
        result = cursor.fetchall()
        cursor.close()
        return result

    def execute_commit(self, query, params=None):
        """Выполняет INSERT, UPDATE или DELETE-запрос с фиксацией изменений."""
        self.connect()
        cursor = self.connection.cursor()
        cursor.execute(query, params)
        self.connection.commit()
        cursor.close()


db_read = Database(dbconfig_read)
db_write = Database(dbconfig_write)


def get_all_genres():
    """Получает список всех жанров."""
    query = "SELECT name FROM category"
    genres = db_read.execute_query(query)
    return [genre["name"] for genre in genres]  # Возвращаем список строк


def get_all_years():
    """Получает список доступных лет фильмов."""
    query = "SELECT DISTINCT release_year FROM film ORDER BY release_year DESC"
    return db_read.execute_query(query)


def get_movies(genre=None, year=None, actor_name=None, offset=0, limit=10):
    """Получает список фильмов с учетом фильтрации по жанру, году и актёру."""
    query = """
        SELECT f.film_id, f.title, f.description, f.release_year, g.name AS genre
        FROM film f
        LEFT JOIN film_category fc ON f.film_id = fc.film_id
        LEFT JOIN category g ON fc.category_id = g.category_id
        WHERE 1=1
    """

    params = []
    if genre:
        query += " AND g.name = %s"
        params.append(genre)
    if year:
        query += " AND f.release_year = %s"
        params.append(year)
    if actor_name:
        query += """
        AND f.film_id IN (
            SELECT fa.film_id FROM film_actor fa
            JOIN actor a ON fa.actor_id = a.actor_id
            WHERE a.first_name LIKE %s OR a.last_name LIKE %s
        )
        """
        params.extend([f"%{actor_name}%", f"%{actor_name}%"])

    query += " LIMIT %s OFFSET %s"
    params.extend([limit, offset])

    movies = db_read.execute_query(query, params)

    # Добавляем список актёров
    for movie in movies:
        actors_query = """
            SELECT a.first_name, a.last_name
            FROM actor a
            JOIN film_actor fa ON a.actor_id = fa.actor_id
            WHERE fa.film_id = %s
        """
        actors = db_read.execute_query(actors_query, (movie["film_id"],))
        movie["actors"] = ", ".join([f"{a['first_name']} {a['last_name']}" for a in actors])

    return movies


# Кэш для популярных запросов
cache = {
    "popular_queries": {"data": None, "timestamp": 0},
}

def get_popular_queries():
    """Получает список популярных запросов с кэшированием (5 минут)."""
    current_time = time.time()

    # Проверяем, есть ли актуальные данные в кэше
    if cache["popular_queries"]["data"] and (current_time - cache["popular_queries"]["timestamp"] < 300):
        return cache["popular_queries"]["data"]

    # Если в кэше нет или данные устарели — делаем запрос
    query = "SELECT query, COUNT(*) AS count FROM Julias_movie_searches GROUP BY query ORDER BY count DESC LIMIT 5;"
    result = db_write.execute_query(query)

    # Обновляем кэш
    cache["popular_queries"]["data"] = result
    cache["popular_queries"]["timestamp"] = current_time

    return result


def save_search_query(query):
    """Сохраняет поисковый запрос в базу данных."""
    query_sql = "INSERT INTO Julias_movie_searches (query) VALUES (%s);"
    try:
        db_write.execute_commit(query_sql, (query,))
    except Exception as e:
        log_error(f"Ошибка при сохранении запроса: {e}")
