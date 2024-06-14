import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from transformers import pipeline, set_seed

load_dotenv()
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')

generator = pipeline('text-generation', model='EleutherAI/gpt-neo-1.3B', truncation=True, pad_token_id=50256)
set_seed(42)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Salute')

async def generate_response(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_input = update.message.text

    prompt = f"Soru: {user_input}\nCevap:"
    response = generator(prompt, max_length=100, num_return_sequences=1)[0]['generated_text']


    answer = response[len(prompt):].strip()

    await update.message.reply_text(answer)

def main() -> None:
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, generate_response))

    application.run_polling()

if __name__ == '__main__':
    main()
