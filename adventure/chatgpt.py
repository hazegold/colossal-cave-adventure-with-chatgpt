import os
import openai
import dotenv

DEBUG=True

dotenv.load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def respond(messages) -> str:
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
    )
    response_message = response["choices"][0]["message"]["content"]
    if DEBUG:
        append_to_file("chatgpt.log", "\n".join([str(m) for m in messages]))
        append_to_file("chatgpt.log", response_message)
    return response_message


def append_to_file(filename, text):
    with open(filename, 'a') as file:
        file.write("!!")
        file.write(text)
        file.write("!!\n")

