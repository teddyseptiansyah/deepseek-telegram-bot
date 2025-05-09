import os
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters

TELEGRAM_TOKEN = os.getenv("7775353801:AAGIHSJsE2YLz_d6PW3eG7-6QmnJWQjz014")
DEEPSEEK_API_KEY = os.getenv("sk-13637f0235c84684b04f8cfb8b8a8cfd")

async def start(update: Update, _):
    await update.message.reply_text("🤖 DeepSeek AI Bot siap membantu!")

async def handle_message(update: Update, _):
    try:
        headers = {"Authorization": f"Bearer {DEEPSEEK_API_KEY}"}
        payload = {
            "model": "deepseek-chat",
            "messages": [{"role": "user", "content": update.message.text}]
        }
        response = requests.post("https://api.deepseek.com/v1/chat/completions", json=payload, headers=headers)
        answer = response.json()["choices"][0]["message"]["content"]
        await update.message.reply_text(answer[:4000])  # Potong jika terlalu panjang
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()
