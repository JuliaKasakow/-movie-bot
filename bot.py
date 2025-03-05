# # import logging
# # from telegram import Update
# # from telegram.ext import Application, CommandHandler, CallbackContext
# #
# # # Включаем логирование
# # logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
# #                     level=logging.INFO)
# # logger = logging.getLogger(__name__)
# #
# # # Функция обработки команды /start
# # async def start(update: Update, context: CallbackContext):
# #     await update.message.reply_text('Привет! Я FilmFinderBot. Введите команду, чтобы начать поиск фильмов.')
# #
# # # Функция обработки команды /help
# # async def help(update: Update, context: CallbackContext):
# #     await update.message.reply_text('Вводите команду для поиска фильмов: \n1. Поиск по ключевому слову \n2. Поиск по жанру и году \n3. Популярные запросы')
# #
# # # Основная функция запуска бота
# # def main():
# #     application = Application.builder().token("TelegrammToken").build()
# #
# #     # Обработчики команд
# #     application.add_handler(CommandHandler("start", start))
# #     application.add_handler(CommandHandler("help", help))
# #
# #     # Запускаем бота
# #     application.run_polling()
# #
# # if __name__ == '__main__':
# #     main()
#
# # import logging
# # from telegram import Update
# # from telegram.ext import Application, CommandHandler, CallbackContext
# # import mysql.connector
# #
# # # Включаем логирование
# # logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
# #                     level=logging.INFO)
# # logger = logging.getLogger(__name__)
# #
# #
# # # Функция обработки команды /start
# # async def start(update: Update, context: CallbackContext):
# #     await update.message.reply_text('Привет! Я FilmFinderBot. Введите команду, чтобы начать поиск фильмов.')
# #
# #
# # # Функция обработки команды /help
# # async def help(update: Update, context: CallbackContext):
# #     await update.message.reply_text(
# #         'Вводите команду для поиска фильмов: \n1. Поиск по ключевому слову \n2. Поиск по жанру и году \n3. Популярные запросы')
# #
# #
# # # Функция для поиска по ключевому слову
# # async def search_by_keyword(update: Update, context: CallbackContext):
# #     query = ' '.join(context.args)
# #
# #     if not query:
# #         await update.message.reply_text('Пожалуйста, укажите ключевое слово для поиска.')
# #         return
# #
# #     # Подключение к базе данных
# #     db = mysql.connector.connect(
# #         host="ich-db.ccegls0svc9m.eu-central-1.rds.amazonaws.com",  # Или твой сервер базы данных
# #         user="ich1",  # Имя пользователя для подключения
# #         password="password",  # Пароль
# #         database="sakila"  # Имя базы данных
# #     )
# #
# #     cursor = db.cursor()
# #     cursor.execute(f"SELECT title FROM film WHERE title LIKE %s LIMIT 10", ('%' + query + '%',))
# #     films = cursor.fetchall()
# #
# #     if films:
# #         results = '\n'.join([film[0] for film in films])
# #         await update.message.reply_text(f"Результаты поиска по '{query}':\n{results}")
# #     else:
# #         await update.message.reply_text(f"По запросу '{query}' ничего не найдено.")
# #
# #     cursor.close()
# #     db.close()
# #
# #
# # # Основная функция запуска бота
# # def main():
# #     application = Application.builder().token("7831708872:AAH8e_ogMmL3iY2IB2M8chWN1Kg1kX6ftAg").build()
# #
# #     # Обработчики команд
# #     application.add_handler(CommandHandler("start", start))
# #     application.add_handler(CommandHandler("help", help))
# #     application.add_handler(CommandHandler("search", search_by_keyword))
# #
# #     # Запускаем бота
# #     application.run_polling()
# #
# #
# # if __name__ == '__main__':
# #     main()
#
#
# import mysql.connector
# from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
# from telegram.ext import Application, CommandHandler, CallbackContext, CallbackQueryHandler, MessageHandler, filters
#
# dbconfig_read = {
#     'host': 'ich-db.ccegls0svc9m.eu-central-1.rds.amazonaws.com',
#     'user': 'ich1',
#     'password': 'password',
#     'database': 'sakila'
# }
#
# def execute_query(query, dbconfig):
#     connection = mysql.connector.connect(**dbconfig)
#     cursor = connection.cursor(dictionary=True)
#     cursor.execute(query)
#     result = cursor.fetchall()
#     cursor.close()
#     connection.close()
#     return result
#
# def get_all_genres():
#     query = "SELECT name FROM category"
#     return execute_query(query, dbconfig_read)
#
# def get_all_years():
#     query = "SELECT DISTINCT release_year FROM film ORDER BY release_year DESC"
#     return execute_query(query, dbconfig_read)
#
# def get_movies(genre=None, year=None, actor_name=None, offset=0):
#     query = f"""
#     SELECT DISTINCT f.title, f.release_year, c.name AS genre
#     FROM film f
#     JOIN film_category fc ON f.film_id = fc.film_id
#     JOIN category c ON fc.category_id = c.category_id
#     LEFT JOIN film_actor fa ON f.film_id = fa.film_id
#     LEFT JOIN actor a ON fa.actor_id = a.actor_id
#     WHERE 1=1
#     """
#
#     if genre:
#         query += f" AND c.name LIKE '%{genre}%'"
#     if year:
#         query += f" AND f.release_year = {year}"
#     if actor_name:
#         query += f" AND (a.first_name LIKE '%{actor_name}%' OR a.last_name LIKE '%{actor_name}%')"
#
#     query += f" LIMIT 10 OFFSET {offset};"
#     return execute_query(query, dbconfig_read)
#
# async def start(update: Update, context: CallbackContext):
#     keyboard = [
#         [InlineKeyboardButton("Выбрать жанр", callback_data="choose_genre")],
#         [InlineKeyboardButton("Выбрать год", callback_data="choose_year")],
#         [InlineKeyboardButton("Выбрать актера", callback_data="choose_actor")]
#     ]
#     await update.message.reply_text(
#         "Привет! Я бот для поиска фильмов. Выберите, что хотите искать:",
#         reply_markup=InlineKeyboardMarkup(keyboard)
#     )
#
# async def genre_choice(update: Update, context: CallbackContext):
#     genres = get_all_genres()
#     keyboard = [[InlineKeyboardButton(genre['name'], callback_data=f"genre_{genre['name']}")] for genre in genres]
#     await update.callback_query.message.reply_text("Выберите жанр:", reply_markup=InlineKeyboardMarkup(keyboard))
#
# async def year_choice(update: Update, context: CallbackContext):
#     years = get_all_years()
#     keyboard = [[InlineKeyboardButton(str(year['release_year']), callback_data=f"year_{year['release_year']}")] for year in years]
#     await update.callback_query.message.reply_text("Выберите год:", reply_markup=InlineKeyboardMarkup(keyboard))
#
# async def actor_choice(update: Update, context: CallbackContext):
#     await update.callback_query.message.reply_text("Напишите имя актера для поиска.")
#
# async def handle_genre(update: Update, context: CallbackContext):
#     genre = update.callback_query.data.split('_')[1]
#     context.user_data['genre'] = genre
#     context.user_data['offset'] = 0
#
#     movies = get_movies(genre=genre)
#
#     if movies:
#         text = "\n".join([f"{movie['title']} ({movie['release_year']})" for movie in movies])
#         keyboard = [
#             [InlineKeyboardButton("Еще 10 фильмов", callback_data="more_movies")],
#             [InlineKeyboardButton("Выбрать год", callback_data="choose_year")],
#             [InlineKeyboardButton("Выбрать актера", callback_data="choose_actor")]
#         ]
#         await update.callback_query.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard))
#     else:
#         await update.callback_query.message.reply_text(f"Фильмы в жанре {genre} не найдены.")
#
# async def handle_year(update: Update, context: CallbackContext):
#     year = update.callback_query.data.split('_')[1]
#     context.user_data['year'] = year
#     context.user_data['offset'] = 0
#
#     movies = get_movies(year=year)
#
#     if movies:
#         text = "\n".join([f"{movie['title']} ({movie['release_year']})" for movie in movies])
#         keyboard = [
#             [InlineKeyboardButton("Еще 10 фильмов", callback_data="more_movies")],
#             [InlineKeyboardButton("Выбрать жанр", callback_data="choose_genre")],
#             [InlineKeyboardButton("Выбрать актера", callback_data="choose_actor")]
#         ]
#         await update.callback_query.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard))
#     else:
#         await update.callback_query.message.reply_text(f"Фильмы за {year} не найдены.")
#
# async def handle_actor(update: Update, context: CallbackContext):
#     actor_name = update.message.text
#     context.user_data['actor_name'] = actor_name
#     context.user_data['offset'] = 0
#
#     movies = get_movies(actor_name=actor_name)
#
#     if movies:
#         text = "\n".join([f"{movie['title']} ({movie['release_year']})" for movie in movies])
#         keyboard = [
#             [InlineKeyboardButton("Еще 10 фильмов", callback_data="more_movies")],
#             [InlineKeyboardButton("Выбрать жанр", callback_data="choose_genre")],
#             [InlineKeyboardButton("Выбрать год", callback_data="choose_year")]
#         ]
#         await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard))
#     else:
#         await update.message.reply_text(f"Фильмы с актером {actor_name} не найдены.")
#
# async def more_movies(update: Update, context: CallbackContext):
#     offset = context.user_data.get('offset', 0) + 10
#     context.user_data['offset'] = offset
#
#     genre = context.user_data.get('genre')
#     year = context.user_data.get('year')
#     actor_name = context.user_data.get('actor_name')
#
#     movies = get_movies(genre=genre, year=year, actor_name=actor_name, offset=offset)
#
#     if movies:
#         text = "\n".join([f"{movie['title']} ({movie['release_year']})" for movie in movies])
#         keyboard = [[InlineKeyboardButton("Еще 10 фильмов", callback_data="more_movies")]]
#         await update.callback_query.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard))
#     else:
#         await update.callback_query.message.reply_text("Больше фильмов не найдено.")
#
# def main():
#     application = Application.builder().token("7831708872:AAH8e_ogMmL3iY2IB2M8chWN1Kg1kX6ftAg").build()
#
#     application.add_handler(CommandHandler("start", start))
#     application.add_handler(CallbackQueryHandler(genre_choice, pattern="choose_genre"))
#     application.add_handler(CallbackQueryHandler(year_choice, pattern="choose_year"))
#     application.add_handler(CallbackQueryHandler(actor_choice, pattern="choose_actor"))
#     application.add_handler(CallbackQueryHandler(handle_genre, pattern="^genre_.*$"))
#     application.add_handler(CallbackQueryHandler(handle_year, pattern="^year_.*$"))
#     application.add_handler(CallbackQueryHandler(more_movies, pattern="more_movies"))
#     application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_actor))
#
#     application.run_polling()
#
# if __name__ == "__main__":
#     main()

# import mysql.connector
# import random
# from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
# from telegram.ext import Application, CommandHandler, CallbackContext, CallbackQueryHandler, MessageHandler, filters
#
# # Настройки подключения к базам данных
# dbconfig_read = {
#     'host': 'ich-db.ccegls0svc9m.eu-central-1.rds.amazonaws.com',
#     'user': 'ich1',
#     'password': 'password',
#     'database': 'sakila'
# }
#
# dbconfig_write = {
#     'host': 'ich-db.ccegls0svc9m.eu-central-1.rds.amazonaws.com',
#     'user': 'ich1',
#     'password': 'password',
#     'database': 'ich_edit'
# }
#
# # Функция для выполнения запросов к базе данных
# def execute_query(query, dbconfig):
#     connection = mysql.connector.connect(**dbconfig)
#     cursor = connection.cursor(dictionary=True)
#     cursor.execute(query)
#     result = cursor.fetchall()
#     cursor.close()
#     connection.close()
#     return result
#
# # Функция сохранения запросов пользователя в базу данных
# def log_search(user_id, query):
#     connection = mysql.connector.connect(**dbconfig_write)  # Используем базу 001_Julia_hr
#     cursor = connection.cursor()
#     cursor.execute("INSERT INTO Julias_movie_searches (user_id, query) VALUES (%s, %s)", (user_id, query))
#     connection.commit()
#     cursor.close()
#     connection.close()
#
# # Функция получения всех жанров
# def get_all_genres():
#     query = "SELECT name FROM category"
#     return execute_query(query, dbconfig_read)
#
# # Функция получения всех годов
# def get_all_years():
#     query = "SELECT DISTINCT release_year FROM film ORDER BY release_year DESC"
#     return execute_query(query, dbconfig_read)
#
# # Функция получения случайного фильма
# def get_random_movie():
#     query = "SELECT f.title, f.description FROM film f ORDER BY RAND() LIMIT 1"
#     return execute_query(query, dbconfig_read)
#
# # Функция получения фильмов по фильтрам
# def get_movies(genre=None, year=None, actor_name=None, offset=0):
#     query = f"""
#     SELECT DISTINCT f.title, f.release_year, c.name AS genre, f.description
#     FROM film f
#     JOIN film_category fc ON f.film_id = fc.film_id
#     JOIN category c ON fc.category_id = c.category_id
#     LEFT JOIN film_actor fa ON f.film_id = fa.film_id
#     LEFT JOIN actor a ON fa.actor_id = a.actor_id
#     WHERE 1=1
#     """
#
#     if genre:
#         query += f" AND c.name LIKE '%{genre}%'"
#     if year:
#         query += f" AND f.release_year = {year}"
#     if actor_name:
#         query += f" AND (a.first_name LIKE '%{actor_name}%' OR a.last_name LIKE '%{actor_name}%')"
#
#     query += f" LIMIT 10 OFFSET {offset};"
#     return execute_query(query, dbconfig_read)
#
# # Функции-обработчики команд
# async def start(update: Update, context: CallbackContext):
#     keyboard = [
#         [InlineKeyboardButton("Выбрать жанр", callback_data="choose_genre")],
#         [InlineKeyboardButton("Выбрать год", callback_data="choose_year")],
#         [InlineKeyboardButton("Выбрать актера", callback_data="choose_actor")],
#         [InlineKeyboardButton("Рандомный фильм", callback_data="random_movie")]
#     ]
#     await update.message.reply_text(
#         "Привет! Я бот для поиска фильмов. Выберите, что хотите искать:",
#         reply_markup=InlineKeyboardMarkup(keyboard)
#     )
#
# async def genre_choice(update: Update, context: CallbackContext):
#     genres = get_all_genres()
#     keyboard = [[InlineKeyboardButton(genre['name'], callback_data=f"genre_{genre['name']}")] for genre in genres]
#     await update.callback_query.message.reply_text("Выберите жанр:", reply_markup=InlineKeyboardMarkup(keyboard))
#
# async def year_choice(update: Update, context: CallbackContext):
#     years = get_all_years()
#     keyboard = [[InlineKeyboardButton(str(year['release_year']), callback_data=f"year_{year['release_year']}")] for year in years]
#     await update.callback_query.message.reply_text("Выберите год:", reply_markup=InlineKeyboardMarkup(keyboard))
#
# async def actor_choice(update: Update, context: CallbackContext):
#     await update.callback_query.message.reply_text("Напишите имя актера для поиска.")
#
# async def handle_genre(update: Update, context: CallbackContext):
#     genre = update.callback_query.data.split('_')[1]
#     context.user_data['genre'] = genre
#     context.user_data['offset'] = 0
#
#     movies = get_movies(genre=genre)
#
#     if movies:
#         text = "\n".join([f"{movie['title']} ({movie['release_year']})\nОписание: {movie['description']}" for movie in movies])
#         keyboard = [
#             [InlineKeyboardButton("Еще 10 фильмов", callback_data="more_movies")],
#             [InlineKeyboardButton("Выбрать год", callback_data="choose_year")],
#             [InlineKeyboardButton("Выбрать актера", callback_data="choose_actor")]
#         ]
#         await update.callback_query.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard))
#     else:
#         await update.callback_query.message.reply_text(f"Фильмы в жанре {genre} не найдены.")
#
# async def handle_year(update: Update, context: CallbackContext):
#     year = update.callback_query.data.split('_')[1]
#     context.user_data['year'] = year
#     context.user_data['offset'] = 0
#
#     movies = get_movies(year=year)
#
#     if movies:
#         text = "\n".join([f"{movie['title']} ({movie['release_year']})\nОписание: {movie['description']}" for movie in movies])
#         keyboard = [
#             [InlineKeyboardButton("Еще 10 фильмов", callback_data="more_movies")],
#             [InlineKeyboardButton("Выбрать жанр", callback_data="choose_genre")],
#             [InlineKeyboardButton("Выбрать актера", callback_data="choose_actor")]
#         ]
#         await update.callback_query.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard))
#     else:
#         await update.callback_query.message.reply_text(f"Фильмы за {year} не найдены.")
#
# async def handle_actor(update: Update, context: CallbackContext):
#     actor_name = update.message.text
#     context.user_data['actor_name'] = actor_name
#     context.user_data['offset'] = 0
#
#     movies = get_movies(actor_name=actor_name)
#
#     if movies:
#         text = "\n".join([f"{movie['title']} ({movie['release_year']})\nОписание: {movie['description']}" for movie in movies])
#         keyboard = [
#             [InlineKeyboardButton("Еще 10 фильмов", callback_data="more_movies")],
#             [InlineKeyboardButton("Выбрать жанр", callback_data="choose_genre")],
#             [InlineKeyboardButton("Выбрать год", callback_data="choose_year")]
#         ]
#         await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard))
#     else:
#         await update.message.reply_text(f"Фильмы с актером {actor_name} не найдены.")
#
# async def more_movies(update: Update, context: CallbackContext):
#     offset = context.user_data.get('offset', 0) + 10
#     context.user_data['offset'] = offset
#
#     genre = context.user_data.get('genre')
#     year = context.user_data.get('year')
#     actor_name = context.user_data.get('actor_name')
#
#     movies = get_movies(genre=genre, year=year, actor_name=actor_name, offset=offset)
#
#     if movies:
#         text = "\n".join([f"{movie['title']} ({movie['release_year']})\nОписание: {movie['description']}" for movie in movies])
#         keyboard = [[InlineKeyboardButton("Еще 10 фильмов", callback_data="more_movies")]]
#         await update.callback_query.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard))
#     else:
#         await update.callback_query.message.reply_text("Больше фильмов не найдено.")
#
# async def random_movie(update: Update, context: CallbackContext):
#     movie = get_random_movie()
#
#     if movie:
#         text = f"{movie[0]['title']}\nОписание: {movie[0]['description']}"
#         await update.callback_query.message.reply_text(text)
#     else:
#         await update.callback_query.message.reply_text("Не удалось найти случайный фильм.")
#
# def main():
#     application = Application.builder().token("7831708872:AAH8e_ogMmL3iY2IB2M8chWN1Kg1kX6ftAg").build()
#
#     application.add_handler(CommandHandler("start", start))
#     application.add_handler(CallbackQueryHandler(genre_choice, pattern="choose_genre"))
#     application.add_handler(CallbackQueryHandler(year_choice, pattern="choose_year"))
#     application.add_handler(CallbackQueryHandler(actor_choice, pattern="choose_actor"))
#     application.add_handler(CallbackQueryHandler(handle_genre, pattern="^genre_.*$"))
#     application.add_handler(CallbackQueryHandler(handle_year, pattern="^year_.*$"))
#     application.add_handler(CallbackQueryHandler(more_movies, pattern="more_movies"))
#     application.add_handler(CallbackQueryHandler(random_movie, pattern="random_movie"))
#     application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_actor))
#
#     application.run_polling()
#
# if __name__ == "__main__":
#     main()
# import mysql.connector
# from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
# from telegram.ext import Application, CommandHandler, CallbackContext, CallbackQueryHandler, MessageHandler, filters
# import random
#
# # Конфигурация базы данных
# dbconfig_read = {
#     'host': 'ich-db.ccegls0svc9m.eu-central-1.rds.amazonaws.com',
#     'user': 'ich1',
#     'password': 'password',
#     'database': 'sakila'
# }
#
# dbconfig_write = {
#     'host': 'ich-db.ccegls0svc9m.eu-central-1.rds.amazonaws.com',
#     'user': 'ich1',
#     'password': 'password',
#     'database': 'ich_edit'
# }
#
# # Функции для работы с базой данных
# def execute_query(query, dbconfig, params=None):
#     try:
#         connection = mysql.connector.connect(**dbconfig)
#         cursor = connection.cursor(dictionary=True)
#         cursor.execute(query, params)
#         result = cursor.fetchall()
#         cursor.close()
#         connection.close()
#         return result
#     except mysql.connector.Error as err:
#         print(f"Error: {err}")
#         return []
#
# # Функции для получения данных из базы
# def get_all_genres():
#     query = "SELECT name FROM category"
#     return execute_query(query, dbconfig_read)
#
# def get_all_years():
#     query = "SELECT DISTINCT release_year FROM film ORDER BY release_year DESC"
#     return execute_query(query, dbconfig_read)
#
# def get_movies(genre=None, year=None, actor_name=None, offset=0):
#     query = """
#     SELECT DISTINCT f.title, f.release_year, c.name AS genre, f.description
#     FROM film f
#     JOIN film_category fc ON f.film_id = fc.film_id
#     JOIN category c ON fc.category_id = c.category_id
#     LEFT JOIN film_actor fa ON f.film_id = fa.film_id
#     LEFT JOIN actor a ON fa.actor_id = a.actor_id
#     WHERE 1=1
#     """
#
#     if genre:
#         query += " AND c.name LIKE %s"
#     if year:
#         query += " AND f.release_year = %s"
#     if actor_name:
#         query += " AND (a.first_name LIKE %s OR a.last_name LIKE %s)"
#
#     query += f" LIMIT 10 OFFSET {offset};"
#
#     params = []
#     if genre:
#         params.append(f"%{genre}%")
#     if year:
#         params.append(year)
#     if actor_name:
#         params.append(f"%{actor_name}%")
#         params.append(f"%{actor_name}%")
#
#     return execute_query(query, dbconfig_read, params)
#
# def get_popular_queries():
#     query = "SELECT query, COUNT(*) AS count FROM search_queries GROUP BY query ORDER BY count DESC LIMIT 5;"
#     return execute_query(query, dbconfig_write)
#
# def save_search_query(query):
#     insert_query = "INSERT INTO search_queries (query) VALUES (%s);"
#     execute_query(insert_query, dbconfig_write, (query,))
#
# def get_random_movie():
#     query = "SELECT title, release_year, description FROM film ORDER BY RAND() LIMIT 1;"
#     return execute_query(query, dbconfig_read)[0]
#
# # Обработчик команд и кнопок
# async def start(update: Update, context: CallbackContext):
#     keyboard = [
#         [InlineKeyboardButton("Выбрать жанр", callback_data="choose_genre")],
#         [InlineKeyboardButton("Выбрать год", callback_data="choose_year")],
#         [InlineKeyboardButton("Выбрать актера", callback_data="choose_actor")],
#         [InlineKeyboardButton("Самые популярные запросы", callback_data="popular_queries")],
#         [InlineKeyboardButton("Рандомный фильм", callback_data="random_movie")]
#     ]
#     await update.message.reply_text(
#         "Привет! Я бот для поиска фильмов. Выберите, что хотите искать:",
#         reply_markup=InlineKeyboardMarkup(keyboard)
#     )
#
# async def genre_choice(update: Update, context: CallbackContext):
#     genres = get_all_genres()
#     keyboard = [[InlineKeyboardButton(genre['name'], callback_data=f"genre_{genre['name']}")] for genre in genres]
#     await update.callback_query.message.reply_text("Выберите жанр:", reply_markup=InlineKeyboardMarkup(keyboard))
#
# async def year_choice(update: Update, context: CallbackContext):
#     years = get_all_years()
#     keyboard = [[InlineKeyboardButton(str(year['release_year']), callback_data=f"year_{year['release_year']}")] for year
#                 in years]
#     await update.callback_query.message.reply_text("Выберите год:", reply_markup=InlineKeyboardMarkup(keyboard))
#
# async def actor_choice(update: Update, context: CallbackContext):
#     await update.callback_query.message.reply_text("Напишите имя актера для поиска.")
#
# async def handle_genre(update: Update, context: CallbackContext):
#     genre = update.callback_query.data.split('_')[1]
#     context.user_data['genre'] = genre
#     context.user_data['offset'] = 0
#
#     save_search_query(f"Жанр: {genre}")
#     movies = get_movies(genre=genre)
#
#     if movies:
#         text = "\n".join([f"{movie['title']} ({movie['release_year']})\n{movie['description']}" for movie in movies])
#         keyboard = [
#             [InlineKeyboardButton("Еще 10 фильмов", callback_data="more_movies")],
#             [InlineKeyboardButton("Выбрать год", callback_data="choose_year")],
#             [InlineKeyboardButton("Выбрать актера", callback_data="choose_actor")]
#         ]
#         await update.callback_query.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard))
#     else:
#         await update.callback_query.message.reply_text(f"Фильмы в жанре {genre} не найдены.")
#
# async def handle_year(update: Update, context: CallbackContext):
#     year = update.callback_query.data.split('_')[1]
#     context.user_data['year'] = year
#     context.user_data['offset'] = 0
#
#     save_search_query(f"Год: {year}")
#     movies = get_movies(year=year)
#
#     if movies:
#         text = "\n".join([f"{movie['title']} ({movie['release_year']})\n{movie['description']}" for movie in movies])
#         keyboard = [
#             [InlineKeyboardButton("Еще 10 фильмов", callback_data="more_movies")],
#             [InlineKeyboardButton("Выбрать жанр", callback_data="choose_genre")],
#             [InlineKeyboardButton("Выбрать актера", callback_data="choose_actor")]
#         ]
#         await update.callback_query.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard))
#     else:
#         await update.callback_query.message.reply_text(f"Фильмы за {year} не найдены.")
#
# async def handle_actor(update: Update, context: CallbackContext):
#     actor_name = update.message.text
#     context.user_data['actor_name'] = actor_name
#     context.user_data['offset'] = 0
#
#     save_search_query(f"Актер: {actor_name}")
#     movies = get_movies(actor_name=actor_name)
#
#     if movies:
#         text = "\n".join([f"{movie['title']} ({movie['release_year']})\n{movie['description']}" for movie in movies])
#         keyboard = [
#             [InlineKeyboardButton("Еще 10 фильмов", callback_data="more_movies")],
#             [InlineKeyboardButton("Выбрать жанр", callback_data="choose_genre")],
#             [InlineKeyboardButton("Выбрать год", callback_data="choose_year")]
#         ]
#         await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard))
#     else:
#         await update.message.reply_text(f"Фильмы с актером {actor_name} не найдены.")
#
# async def more_movies(update: Update, context: CallbackContext):
#     offset = context.user_data.get('offset', 0) + 10
#     context.user_data['offset'] = offset
#
#     genre = context.user_data.get('genre')
#     year = context.user_data.get('year')
#     actor_name = context.user_data.get('actor_name')
#
#     movies = get_movies(genre=genre, year=year, actor_name=actor_name, offset=offset)
#
#     if movies:
#         text = "\n".join([f"{movie['title']} ({movie['release_year']})\n{movie['description']}" for movie in movies])
#         keyboard = [[InlineKeyboardButton("Еще 10 фильмов", callback_data="more_movies")]]
#         await update.callback_query.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard))
#     else:
#         await update.callback_query.message.reply_text("Больше фильмов не найдено.")
#
# async def popular_queries(update: Update, context: CallbackContext):
#     queries = get_popular_queries()
#     if queries:
#         text = "\n".join([f"{query['query']} - {query['count']} запросов" for query in queries])
#         await update.callback_query.message.reply_text(f"Популярные запросы:\n{text}")
#     else:
#         await update.callback_query.message.reply_text("Популярных запросов не найдено.")
#
# async def random_movie(update: Update, context: CallbackContext):
#     movie = get_random_movie()
#     text = f"Рандомный фильм:\n{movie['title']} ({movie['release_year']})\n{movie['description']}"
#     await update.callback_query.message.reply_text(text)
#
# # Запуск бота
# def main():
#     application = Application.builder().token("7831708872:AAH8e_ogMmL3iY2IB2M8chWN1Kg1kX6ftAg").build()
#
#     application.add_handler(CommandHandler("start", start))
#     application.add_handler(CallbackQueryHandler(genre_choice, pattern="choose_genre"))
#     application.add_handler(CallbackQueryHandler(year_choice, pattern="choose_year"))
#     application.add_handler(CallbackQueryHandler(actor_choice, pattern="choose_actor"))
#     application.add_handler(CallbackQueryHandler(handle_genre, pattern="genre_"))
#     application.add_handler(CallbackQueryHandler(handle_year, pattern="year_"))
#     application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_actor))
#     application.add_handler(CallbackQueryHandler(more_movies, pattern="more_movies"))
#     application.add_handler(CallbackQueryHandler(popular_queries, pattern="popular_queries"))
#     application.add_handler(CallbackQueryHandler(random_movie, pattern="random_movie"))
#
#     application.run_polling()
#
# if __name__ == '__main__':
#     main()
#

# import mysql.connector
# from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
# from telegram.ext import Application, CommandHandler, CallbackContext, CallbackQueryHandler, MessageHandler, filters
# import random
#
# # Конфигурация базы данных
# dbconfig_read = {
#     'host': 'ich-db.ccegls0svc9m.eu-central-1.rds.amazonaws.com',
#     'user': 'ich1',
#     'password': 'password',
#     'database': 'sakila'
# }
#
# dbconfig_write = {
#     'host': 'ich-db.ccegls0svc9m.eu-central-1.rds.amazonaws.com',
#     'user': 'ich1',
#     'password': 'password',
#     'database': 'ich_edit'
# }
#
#
# # Функции для работы с базой данных
# def execute_query(query, dbconfig, params=None):
#     connection = mysql.connector.connect(**dbconfig)
#     cursor = connection.cursor(dictionary=True)
#     cursor.execute(query, params)
#     result = cursor.fetchall()
#     cursor.close()
#     connection.close()
#     return result
#
#
# # Функции для получения данных из базы
# def get_all_genres():
#     query = "SELECT name FROM category"
#     return execute_query(query, dbconfig_read)
#
#
# def get_all_years():
#     query = "SELECT DISTINCT release_year FROM film ORDER BY release_year DESC"
#     return execute_query(query, dbconfig_read)
#
#
# def get_movies(genre=None, year=None, actor_name=None, offset=0):
#     query = """
#     SELECT DISTINCT f.title, f.release_year, c.name AS genre, f.description
#     FROM film f
#     JOIN film_category fc ON f.film_id = fc.film_id
#     JOIN category c ON fc.category_id = c.category_id
#     LEFT JOIN film_actor fa ON f.film_id = fa.film_id
#     LEFT JOIN actor a ON fa.actor_id = a.actor_id
#     WHERE 1=1
#     """
#
#     if genre:
#         query += f" AND c.name LIKE %s"
#     if year:
#         query += f" AND f.release_year = %s"
#     if actor_name:
#         query += f" AND (a.first_name LIKE %s OR a.last_name LIKE %s)"
#
#     query += f" LIMIT 10 OFFSET {offset};"
#
#     params = []
#     if genre:
#         params.append(f"%{genre}%")
#     if year:
#         params.append(year)
#     if actor_name:
#         params.append(f"%{actor_name}%")
#         params.append(f"%{actor_name}%")
#
#     return execute_query(query, dbconfig_read, params)
#
#
# def get_popular_queries():
#     query = "SELECT query, COUNT(*) AS count FROM Julias_movie_searches GROUP BY query ORDER BY count DESC LIMIT 5;"
#     return execute_query(query, dbconfig_write)
#
#
# def save_search_query(query):
#     query_sql = "INSERT INTO Julias_movie_searches (query) VALUES (%s);"
#     try:
#         connection = mysql.connector.connect(**dbconfig_write)
#         cursor = connection.cursor()
#         cursor.execute(query_sql, (query,))
#         connection.commit()  # Сохраняем изменения
#         cursor.close()
#         connection.close()
#     except Exception as e:
#         print(f"Error saving query: {e}")
#
#
# def get_random_movie():
#     query = "SELECT title, release_year, description FROM film ORDER BY RAND() LIMIT 1;"
#     return execute_query(query, dbconfig_read)[0]
#
#
# # Обработчик команд и кнопок
# async def start(update: Update, context: CallbackContext):
#     keyboard = [
#         [InlineKeyboardButton("Выбрать жанр", callback_data="choose_genre")],
#         [InlineKeyboardButton("Выбрать год", callback_data="choose_year")],
#         [InlineKeyboardButton("Выбрать актера", callback_data="choose_actor")],
#         [InlineKeyboardButton("Самые популярные запросы", callback_data="popular_queries")],
#         [InlineKeyboardButton("Рандомный фильм", callback_data="random_movie")]
#     ]
#     await update.message.reply_text(
#         "Привет! Я бот для поиска фильмов. Выберите, что хотите искать:",
#         reply_markup=InlineKeyboardMarkup(keyboard)
#     )
#
#
# async def genre_choice(update: Update, context: CallbackContext):
#     genres = get_all_genres()
#     keyboard = [[InlineKeyboardButton(genre['name'], callback_data=f"genre_{genre['name']}")] for genre in genres]
#     await update.callback_query.message.reply_text("Выберите жанр:", reply_markup=InlineKeyboardMarkup(keyboard))
#
#
# async def year_choice(update: Update, context: CallbackContext):
#     years = get_all_years()
#     keyboard = [[InlineKeyboardButton(str(year['release_year']), callback_data=f"year_{year['release_year']}")] for year
#                 in years]
#     await update.callback_query.message.reply_text("Выберите год:", reply_markup=InlineKeyboardMarkup(keyboard))
#
#
# async def actor_choice(update: Update, context: CallbackContext):
#     await update.callback_query.message.reply_text("Напишите имя актера для поиска.")
#
#
# async def handle_genre(update: Update, context: CallbackContext):
#     genre = update.callback_query.data.split('_')[1]
#     context.user_data['genre'] = genre
#     context.user_data['offset'] = 0
#
#     save_search_query(f"Жанр: {genre}")
#     movies = get_movies(genre=genre)
#
#     if movies:
#         text = "\n".join([f"{movie['title']} ({movie['release_year']})\n{movie['description']}" for movie in movies])
#         keyboard = [
#             [InlineKeyboardButton("Еще 10 фильмов", callback_data="more_movies")],
#             [InlineKeyboardButton("Выбрать год", callback_data="choose_year")],
#             [InlineKeyboardButton("Выбрать актера", callback_data="choose_actor")]
#         ]
#         await update.callback_query.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard))
#     else:
#         await update.callback_query.message.reply_text(f"Фильмы в жанре {genre} не найдены.")
#
#
# async def handle_year(update: Update, context: CallbackContext):
#     year = update.callback_query.data.split('_')[1]
#     context.user_data['year'] = year
#     context.user_data['offset'] = 0
#
#     save_search_query(f"Год: {year}")
#     movies = get_movies(year=year)
#
#     if movies:
#         text = "\n".join([f"{movie['title']} ({movie['release_year']})\n{movie['description']}" for movie in movies])
#         keyboard = [
#             [InlineKeyboardButton("Еще 10 фильмов", callback_data="more_movies")],
#             [InlineKeyboardButton("Выбрать жанр", callback_data="choose_genre")],
#             [InlineKeyboardButton("Выбрать актера", callback_data="choose_actor")]
#         ]
#         await update.callback_query.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard))
#     else:
#         await update.callback_query.message.reply_text(f"Фильмы за {year} не найдены.")
#
#
# async def handle_actor(update: Update, context: CallbackContext):
#     actor_name = update.message.text  # Получаем имя актера из текста сообщения
#     context.user_data['actor_name'] = actor_name
#     context.user_data['offset'] = 0
#
#     save_search_query(f"Актер: {actor_name}")
#     movies = get_movies(actor_name=actor_name)
#
#     if movies:
#         text = "\n".join([f"{movie['title']} ({movie['release_year']})\n{movie['description']}" for movie in movies])
#         keyboard = [
#             [InlineKeyboardButton("Еще 10 фильмов", callback_data="more_movies")],
#             [InlineKeyboardButton("Выбрать жанр", callback_data="choose_genre")],
#             [InlineKeyboardButton("Выбрать год", callback_data="choose_year")]
#         ]
#         await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard))  # Используем update.message
#     else:
#         await update.message.reply_text(f"Фильмы с актером {actor_name} не найдены.")  # Используем update.message
#
#
# async def more_movies(update: Update, context: CallbackContext):
#     offset = context.user_data.get('offset', 0) + 10
#     context.user_data['offset'] = offset
#
#     genre = context.user_data.get('genre')
#     year = context.user_data.get('year')
#     actor_name = context.user_data.get('actor_name')
#
#     movies = get_movies(genre=genre, year=year, actor_name=actor_name, offset=offset)
#
#     if movies:
#         text = "\n".join([f"{movie['title']} ({movie['release_year']})\n{movie['description']}" for movie in movies])
#         keyboard = [[InlineKeyboardButton("Еще 10 фильмов", callback_data="more_movies")]]
#         await update.callback_query.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard))
#     else:
#         await update.callback_query.message.reply_text("Больше фильмов не найдено.")
#
#
# async def popular_queries(update: Update, context: CallbackContext):
#     queries = get_popular_queries()
#     if queries:
#         text = "\n".join(
#             [f"{i + 1}. {query['query']} (поиск выполнен {query['count']} раз)" for i, query in enumerate(queries)])
#         await update.callback_query.message.reply_text(f"Самые популярные запросы:\n{text}")
#     else:
#         await update.callback_query.message.reply_text("Популярные запросы не найдены.")
#
#
# async def random_movie(update: Update, context: CallbackContext):
#     movie = get_random_movie()
#     text = f"{movie['title']} ({movie['release_year']})\n{movie['description']}"
#     await update.callback_query.message.reply_text(f"Случайный фильм:\n{text}")
#
#
# def main():
#     application = Application.builder().token("7831708872:AAH8e_ogMmL3iY2IB2M8chWN1Kg1kX6ftAg").build()
#
#     application.add_handler(CommandHandler("start", start))
#     application.add_handler(CallbackQueryHandler(genre_choice, pattern="choose_genre"))
#     application.add_handler(CallbackQueryHandler(year_choice, pattern="choose_year"))
#     application.add_handler(CallbackQueryHandler(actor_choice, pattern="choose_actor"))
#     application.add_handler(CallbackQueryHandler(popular_queries, pattern="popular_queries"))
#     application.add_handler(CallbackQueryHandler(random_movie, pattern="random_movie"))
#     application.add_handler(CallbackQueryHandler(handle_genre, pattern="^genre_.*$"))
#     application.add_handler(CallbackQueryHandler(handle_year, pattern="^year_.*$"))
#     application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_actor))
#     application.add_handler(CallbackQueryHandler(more_movies, pattern="more_movies"))
#
#     application.run_polling()
#
#
# if __name__ == "__main__":
#     main()
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters
from handlers import start, genre_choice, year_choice, actor_choice, handle_genre, handle_year, handle_actor, \
    more_movies, popular_queries, stop_bot, handle_greeting, handle_start_press

def main():
    application = Application.builder().token("7831708872:AAH8e_ogMmL3iY2IB2M8chWN1Kg1kX6ftAg").build()

    # **Обработчик первого входа в бота** (новый пользователь увидит кнопку "Старт")
    application.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, start))

    # **Команды и сообщения**
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.Regex(r'(?i)^привет|здравствуй|здравствуйте'), handle_greeting))
    application.add_handler(MessageHandler(filters.Regex(r'(?i)^старт$'), handle_start_press))

    # **Кнопки меню**
    application.add_handler(CallbackQueryHandler(genre_choice, pattern="choose_genre"))
    application.add_handler(CallbackQueryHandler(year_choice, pattern="choose_year"))
    application.add_handler(CallbackQueryHandler(actor_choice, pattern="choose_actor"))
    application.add_handler(CallbackQueryHandler(popular_queries, pattern="popular_queries"))
    application.add_handler(CallbackQueryHandler(handle_genre, pattern="^genre_.*$"))
    application.add_handler(CallbackQueryHandler(handle_year, pattern="^year_.*$"))
    application.add_handler(CallbackQueryHandler(more_movies, pattern="more_movies"))
    application.add_handler(CallbackQueryHandler(stop_bot, pattern="stop"))

    # **Поиск по тексту (например, по имени актера)**
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_actor))

    application.run_polling()

if __name__ == "__main__":
    main()
