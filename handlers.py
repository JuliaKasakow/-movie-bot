from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.ext import CallbackContext
from database import get_all_genres, get_all_years, get_movies, get_popular_queries, save_search_query
from utils import log_info, format_movie_info


def get_start_keyboard():
    """Возвращает клавиатуру с кнопкой 'Старт'."""
    return ReplyKeyboardMarkup([['Старт']], resize_keyboard=True)


async def start(update: Update, context: CallbackContext):
    """Обработчик команды /start и первого входа в бота."""
    await update.message.reply_text(
        "Привет! Нажмите кнопку 'Старт', чтобы начать работу с ботом.",
        reply_markup=get_start_keyboard()
    )


async def handle_start_press(update: Update, context: CallbackContext):
    """Обрабатывает нажатие кнопки 'Старт' и загружает меню."""
    await show_menu(update, context)


async def show_menu(update: Update, context: CallbackContext):
    """Отправляет основное меню после выбора опции."""
    keyboard = [
        [InlineKeyboardButton("🎭 Найти по жанру", callback_data="choose_genre")],
        [InlineKeyboardButton("📅 Найти по году", callback_data="choose_year")],
        [InlineKeyboardButton("🎬 Найти по актеру", callback_data="choose_actor")],
        [InlineKeyboardButton("🔥 Популярные запросы", callback_data="popular_queries")],
        [InlineKeyboardButton("❌ Закончить работу", callback_data="stop")]
    ]

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Выберите действие:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def genre_choice(update: Update, context: CallbackContext):
    """Выводит список жанров."""
    genres = get_all_genres()
    if not genres:
        await update.callback_query.message.reply_text("Жанры не найдены.")
        return

    keyboard = [[InlineKeyboardButton(genre, callback_data=f"genre_{genre}")] for genre in genres]
    await update.callback_query.message.reply_text("Выберите жанр:", reply_markup=InlineKeyboardMarkup(keyboard))

async def handle_genre(update: Update, context: CallbackContext):
    """Выводит список фильмов по выбранному жанру."""
    genre = update.callback_query.data.split('_')[1]
    context.user_data.update({'genre': genre, 'offset': 0})

    user_id = update.effective_user.id
    log_info(f"Пользователь {user_id} выбрал жанр: {genre}")

    save_search_query(f"Жанр: {genre}")
    movies = get_movies(genre=genre, offset=0)

    if not movies:
        await update.callback_query.message.reply_text(f"Фильмы в жанре {genre} не найдены.")
    else:
        text = "\n\n".join([format_movie_info(movie) for movie in movies])
        await update.callback_query.message.reply_text(text, parse_mode="Markdown")

    await show_menu(update, context)

async def year_choice(update: Update, context: CallbackContext):
    """Выводит список годов."""
    years = get_all_years()
    if not years:
        await update.callback_query.message.reply_text("Годы не найдены.")
        return

    keyboard = [[InlineKeyboardButton(str(year['release_year']), callback_data=f"year_{year['release_year']}")] for year in years]
    await update.callback_query.message.reply_text("Выберите год:", reply_markup=InlineKeyboardMarkup(keyboard))

async def handle_year(update: Update, context: CallbackContext):
    """Выводит список фильмов по выбранному году."""
    year = update.callback_query.data.split('_')[1]
    context.user_data.update({'year': year, 'offset': 0})

    user_id = update.effective_user.id
    log_info(f"Пользователь {user_id} выбрал год: {year}")

    save_search_query(f"Год: {year}")
    movies = get_movies(year=year, offset=0)

    if not movies:
        await update.callback_query.message.reply_text(f"Фильмы за {year} не найдены.")
    else:
        text = "\n\n".join([format_movie_info(movie) for movie in movies])
        await update.callback_query.message.reply_text(text, parse_mode="Markdown")

    await show_menu(update, context)

async def actor_choice(update: Update, context: CallbackContext):
    """Запрашивает ввод имени актера с подсказкой о языке."""
    await update.callback_query.message.reply_text(
        "Введите имя актера на *английском языке* (например, `Tom Hanks`).",
        parse_mode="Markdown"
    )

async def handle_actor(update: Update, context: CallbackContext):
    """Выводит список фильмов по введенному актеру."""
    actor_name = update.message.text
    context.user_data.update({'actor_name': actor_name, 'offset': 0})

    user_id = update.effective_user.id
    log_info(f"Пользователь {user_id} ищет фильмы с актером: {actor_name}")

    save_search_query(f"Актер: {actor_name}")
    movies = get_movies(actor_name=actor_name, offset=0)

    if not movies:
        await update.message.reply_text(f"Фильмы с актером {actor_name} не найдены.")
    else:
        text = "\n\n".join([format_movie_info(movie) for movie in movies])
        await update.message.reply_text(text, parse_mode="Markdown")

    await show_menu(update, context)

async def more_movies(update: Update, context: CallbackContext):
    """Выводит дополнительные фильмы."""
    context.user_data['offset'] += 10
    genre, year, actor_name = context.user_data.get('genre'), context.user_data.get('year'), context.user_data.get('actor_name')

    movies = get_movies(genre=genre, year=year, actor_name=actor_name, offset=context.user_data['offset'])

    if not movies:
        await update.callback_query.message.reply_text("Больше фильмов не найдено.")
    else:
        text = "\n\n".join([format_movie_info(movie) for movie in movies])
        await update.callback_query.message.reply_text(text, parse_mode="Markdown")

    await show_menu(update, context)

async def popular_queries(update: Update, context: CallbackContext):
    """Выводит популярные запросы."""
    user_id = update.effective_user.id
    log_info(f"Пользователь {user_id} запросил популярные поиски")

    queries = get_popular_queries()

    if not queries:
        await update.callback_query.message.reply_text("Популярные запросы не найдены.")
    else:
        text = "🔥 *Самые популярные запросы:*\n\n" + "\n".join(
            [f"🔹 {i + 1}. `{query['query']}` (🔍 {query['count']} раз)" for i, query in enumerate(queries)]
        )
        await update.callback_query.message.reply_text(text, parse_mode="Markdown")

    await show_menu(update, context)

async def stop_bot(update: Update, context: CallbackContext):
    """Завершает работу бота и отправляет сообщение."""
    query = update.callback_query
    await query.answer()  # Подтверждает нажатие кнопки

    # Убираем inline-кнопки (чтобы не висели после нажатия "Закончить работу")
    await query.message.edit_reply_markup(reply_markup=None)

    # Отправляем финальное сообщение
    await query.message.reply_text("❌ Бот завершил работу. До встречи! 👋")

async def handle_greeting(update: Update, context: CallbackContext):
    """Отвечает на приветствие и предлагает меню."""
    await update.message.reply_text("Привет! Чем могу помочь? Вы можете нажать 'Старт' внизу экрана.")

