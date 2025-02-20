import telebot
import google.generativeai as genai
import logging

# 📌 Log faylni sozlash (barcha xatolar va xabarlar shu faylga yoziladi)
logging.basicConfig(
    filename="bot.log",  # Log fayl nomi
    level=logging.INFO,   # INFO va ERROR loglarini yozish
    format="%(asctime)s - %(levelname)s - %(message)s",  # Vaqt va log darajasini ko‘rsatish
)

# API kalitlari
TELEGRAM_BOT_TOKEN = "7922800148:AAFVxdO5Fhngr5Z01Iih93I77ocsrD5mHBI"
GENAI_API_KEY = "AIzaSyBhIdylhY9s1ax1cXnA8AdCSJCZrUVOT7g"

# Telegram botni yaratish
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN, parse_mode="Markdown")

# Google Gemini sozlamalari
genai.configure(api_key=GENAI_API_KEY)

generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 1024,
    "response_mime_type": "text/plain",
}

# Modelni yaratish
model = genai.GenerativeModel(
    model_name="gemini-2.0-flash",
    generation_config=generation_config,
    system_instruction="Salom, men chat botman! Sizga qanday yordam bera olaman?",
)

chat_session = model.start_chat(history=[])

# Xabarni qayta ishlash funksiyasi
def generate_response(text):
    if not text.strip():  # Bo‘sh xabar yuborilganda
        return "Iltimos, savolingizni aniqroq yozing."

    try:
        response = chat_session.send_message(text)
        if response and response.text:  # Javob bo‘lsa
            return response.text.strip()
        else:
            return "Kechirasiz, men bu savolga javob topa olmadim."
    except Exception as e:
        logging.error(f"Xatolik yuz berdi: {e}")  # Xatolikni logga yozish
        return "Kechirasiz, texnik xatolik yuz berdi. Keyinroq urinib ko‘ring."

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    logging.info(f"Foydalanuvchi: {message.chat.id}, Xabar: {message.text}")  # Foydalanuvchi xabarini logga yozish
    response = generate_response(message.text)
    bot.reply_to(message, response)
    logging.info(f"Bot javobi: {response}")  # Botning javobini logga yozish

# Botni ishga tushirish
if __name__ == "__main__":
    logging.info("Bot ishga tushdi...")  # Bot ishga tushganini logga yozish
    while True:
        try:
            bot.infinity_polling(timeout=10, long_polling_timeout=5)
        except Exception as e:
            logging.error(f"Bot ishlamay qoldi, qayta ishga tushmoqda: {e}")  # Xatolikni logga yozish
