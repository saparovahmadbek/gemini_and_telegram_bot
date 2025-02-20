import os
import google.generativeai as genai

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

response = chat_session.send_message("salom sizga qanday yordam bera olaman")

print(response.text)