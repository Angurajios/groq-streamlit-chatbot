import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
api_key = os.getenv("Groq_api")
client = Groq(api_key=api_key)

messages = [{"role": "system", "content": "you are a helpful assistant"}]

while True:
    user_input = input("User: ")

    if user_input.lower() in ("exit", "quit"):
        break

    messages.append({"role": "user", "content": user_input})

    completion = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=messages
    )

    reply = completion.choices[0].message.content
    messages.append({"role": "assistant", "content": reply})
    print("Bot:", reply)