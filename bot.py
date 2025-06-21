print("STARTING BOT...")

import os
import sys

BOT_TOKEN = os.getenv("BOT_TOKEN")
print(f"BOT_TOKEN = {BOT_TOKEN}", file=sys.stderr)

if not BOT_TOKEN:
    print("Ошибка: переменная окружения BOT_TOKEN не установлена!", file=sys.stderr)
    exit(1)
    
from telegram import Update, User, ChatMember, ChatMemberUpdated
from telegram.ext import (
    Application,
    ContextTypes,
    ChatMemberHandler,
    CommandHandler,
)

BOT_TOKEN = os.getenv("BOT_TOKEN")  # Читаем токен из переменной окружения
REKLAMA_CONTACT = "@aburkas"

# Обработка нового участника
async def welcome_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
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

# Команда /testnew — эмуляция нового участника
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

if __name__ == "__main__":
    if not BOT_TOKEN:
        print("Ошибка: переменная окружения BOT_TOKEN не установлена!")
        exit(1)

    print("STARTING BOT...")
    app = Application.builder().token(BOT_TOKEN).build()

    # Обработка настоящих новых участников
    app.add_handler(ChatMemberHandler(welcome_user, ChatMemberHandler.CHAT_MEMBER))

    # Обработка команды /testnew
    app.add_handler(CommandHandler("testnew", test_new_user))

    print("Бот запущен.")
    app.run_polling()
