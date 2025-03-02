import logging
import time
from deep_translator import GoogleTranslator

# Настройка логирования
logging.basicConfig(
    filename="bot_logs.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8"
)

# Кэш переведённых строк
translation_cache = {}

def translate_text(text, dest_lang="ru"):
    """Переводит текст с использованием deep-translator и кэша"""
    if not text:  # Проверяем, есть ли текст
        return text

    if text in translation_cache:
        return translation_cache[text]

    try:
        start_time = time.time()
        translated = GoogleTranslator(source="auto", target=dest_lang).translate(text)
        end_time = time.time()
        log_info(f"Перевод текста '{text}' занял {round(end_time - start_time, 2)} секунд")
        translation_cache[text] = translated
        return translated
    except Exception as e:
        log_error(f"Ошибка перевода текста '{text}': {e}")
        return text  # Возвращаем оригинальный текст в случае ошибки

def log_info(message):
    """Записывает информационные сообщения в лог"""
    logging.info(message)

def log_error(error):
    """Записывает ошибки в лог"""
    logging.error(error)

def format_movie_info(movie):
    """Форматирует информацию о фильме с переводом и актёрами"""
    title_ru = translate_text(movie["title"])
    description_ru = translate_text(movie["description"])

    return (
        f"🎬 {movie['title']} ({title_ru}) ({movie['release_year']})\n"
        f"📌 Жанр: {movie['genre']}\n"
        f"📝 Описание: {description_ru}\n"
        f"🎭 Актёры: {movie['actors']}"
    )
