import telebot
import google.generativeai as genai
import time
import logging
import threading
import requests

# Logger sozlamalari
logging.basicConfig(level=logging.INFO)

# Tokenlar
TELEGRAM_BOT_TOKEN = "7922800148:AAFVxdO5Fhngr5Z01Iih93I77ocsrD5mHBI"
GENAI_API_KEY = "AIzaSyBhIdylhY9s1ax1cXnA8AdCSJCZrUVOT7g"

# Bot va Gemini sozlamalari
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN, parse_mode="HTML")
genai.configure(api_key=GENAI_API_KEY)

# Gemini modeli sozlamalari
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-2.0-flash",
    generation_config=generation_config,
    system_instruction="Salom! Men chat botman. Qanday yordam bera olaman?",
)

chat_session = model.start_chat(history=[
    {"role": "user", "parts": ["Salom!"]},
    {"role": "model", "parts": ["Salom! Qanday yordam bera olaman?"]},
])

# Keep-alive funksiyasi (botni ping qilish)
def ping_render():
    while True:
        try:
            requests.get("https://gemini-and-telegram-bot-35ac.onrender.com")  # URL-ni o'zgartiring
            logging.info("Ping yuborildi")
            time.sleep(600)  # Har 10 daqiqada ping yuboradi
        except Exception as e:
            logging.error(f"Ping xatosi: {e}")

threading.Thread(target=ping_render, daemon=True).start()

# Xabarlarni qayta ishlash
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        logging.info(f"Yangi xabar: {message.text}")
        response = chat_session.send_message(message.text)
        bot.reply_to(message, response.text)
    except Exception as e:
        logging.error(f"Xatolik yuz berdi: {e}")
        bot.reply_to(message, "Kechirasiz, xatolik yuz berdi. Keyinroq urinib ko'ring.")

# Botni doimiy ravishda ishga tushirish
while True:
    try:
        logging.info("Bot ishga tushdi...")
        bot.infinity_polling(timeout=30, long_polling_timeout=25)
    except Exception as e:
        logging.error(f"Botda xatolik: {e}")
        time.sleep(5)  # Xatolik bo'lsa, 5 soniyadan so'ng qayta ishga tushadi
