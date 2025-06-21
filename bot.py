from telegram import Update
from telegram.ext import Application, ChatMemberHandler, ContextTypes

BOT_TOKEN = "7516479313:AAGFunEzIlXOf5uJTVFcE31ongvacEJ0dJM"
REKLAMA_CONTACT = "@aburkas"

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

if __name__ == "__main__":
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(ChatMemberHandler(welcome_user, ChatMemberHandler.CHAT_MEMBER))
    print("Бот запущен.")
    app.run_polling()
