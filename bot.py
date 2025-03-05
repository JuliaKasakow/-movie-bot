from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters
from handlers import start, genre_choice, year_choice, actor_choice, handle_genre, handle_year, handle_actor, \
    more_movies, popular_queries, stop_bot, handle_greeting, handle_start_press

def main():
    application = Application.builder().token("Токен").build()

    application.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, start))

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.Regex(r'(?i)^привет|здравствуй|здравствуйте'), handle_greeting))
    application.add_handler(MessageHandler(filters.Regex(r'(?i)^старт$'), handle_start_press))

    application.add_handler(CallbackQueryHandler(genre_choice, pattern="choose_genre"))
    application.add_handler(CallbackQueryHandler(year_choice, pattern="choose_year"))
    application.add_handler(CallbackQueryHandler(actor_choice, pattern="choose_actor"))
    application.add_handler(CallbackQueryHandler(popular_queries, pattern="popular_queries"))
    application.add_handler(CallbackQueryHandler(handle_genre, pattern="^genre_.*$"))
    application.add_handler(CallbackQueryHandler(handle_year, pattern="^year_.*$"))
    application.add_handler(CallbackQueryHandler(more_movies, pattern="more_movies"))
    application.add_handler(CallbackQueryHandler(stop_bot, pattern="stop"))

    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_actor))

    application.run_polling()

if __name__ == "__main__":
    main()
