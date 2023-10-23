import os
import openai
import dotenv

DEBUG=True

dotenv.load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def respond(system_prompt, user_input) -> str:
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input},
        ]
    )
    response_message = response["choices"][0]["message"]["content"]
    if DEBUG:
        append_to_file("chatgpt.log", system_prompt)
        append_to_file("chatgpt.log", user_input)
        append_to_file("chatgpt.log", response_message)
    return response_message


def append_to_file(filename, text):
    with open(filename, 'a') as file:
        file.write(text)
        file.write("\n\n")

