import telebot
import google.generativeai as genai
import os

bot = telebot.TeleBot("7922800148:AAFVxdO5Fhngr5Z01Iih93I77ocsrD5mHBI", parse_mode=None)
# You can set parse_mode by default. HTML or MARKDOWN
genai.configure(api_key="AIzaSyBhIdylhY9s1ax1cXnA8AdCSJCZrUVOT7g")

# Create the model
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
  system_instruction="salom men chat botman\n",
)

chat_session = model.start_chat(
  history=[
    {
      "role": "user",
      "parts": [
        "salom men chat botman\n",
      ],
    },
    {
      "role": "model",
      "parts": [
        "Men ham chat botman! Qanday yordam bera olaman?\n",
      ],
    },
  ]
)
@bot.message_handler(func=lambda m: True)
def echo_all(message):
	response = chat_session.send_message(message.text)

	response=(response.text)
	bot.reply_to(message, response)
bot.infinity_polling()