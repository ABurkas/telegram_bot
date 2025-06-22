print("STARTING BOT...")

BOT_TOKEN = "7516479313:AAGFunEzIlXOf5uJTVFcE31ongvacEJ0dJM"  # Вставь сюда свой токен

if not BOT_TOKEN:
    print("Ошибка: токен не указан!")
    exit(1)

from telegram import Update, User, ChatMember, ChatMemberUpdated
from telegram.ext import (
    Application,
    ContextTypes,
    ChatMemberHandler,
    CommandHandler,
)

REKLAMA_CONTACT = "@aburkas"

# Обработка нового участника — пишем в группу
async def welcome_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("Новое событие chat_member:")
    print(update.chat_member)

    member_status = update.chat_member
    new_member = member_status.new_chat_member

    if new_member.status == "member":
        user = new_member.user
        chat_id = member_status.chat.id

        message = (
            f"👋 Добро пожаловать, {user.mention_html()}!\n\n"
            f"Если вы хотите разместить рекламу — напишите {REKLAMA_CONTACT}."
        )

        await context.bot.send_message(chat_id=chat_id, text=message, parse_mode="HTML")
        print("Приветствие отправлено в группу ✅")

# /testnew — тест приветствия
async def test_new_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("Получена команда /testnew")
    fake_user = User(id=123456789, is_bot=False, first_name="Тест", username="testuser")
    fake_chat = update.effective_chat

    chat_member = ChatMemberUpdated(
        chat=fake_chat,
        from_user=fake_user,
        date=update.effective_message.date,
        old_chat_member=ChatMember(status="left", user=fake_user),
        new_chat_member=ChatMember(status="member", user=fake_user),
    )

    fake_update = Update(update.update_id, chat_member=chat_member)
    await welcome_user(fake_update, context)

# /start — проверка работы
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Бот работает!")

# Запуск бота
if __name__ == "__main__":
    print("STARTING BOT...")
    app = Application.builder().token(BOT_TOKEN).build()

    # Обработка новых участников
    app.add_handler(ChatMemberHandler(welcome_user, ChatMemberHandler.CHAT_MEMBER | ChatMemberHandler.MY_CHAT_MEMBER))

    # Команды
    app.add_handler(CommandHandler("testnew", test_new_user))
    app.add_handler(CommandHandler("start", start))

    print("Бот запущен.")
    app.run_polling()
