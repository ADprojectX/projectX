import openai
import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.getcwd(), ".env")
load_dotenv(dotenv_path)


def request_script(text):
    openai.api_key = os.getenv("OPENAI_SECRET_KEY")
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You will act as a youtube expert who will generate a script perfectly for the topic given",
            },
            {"role": "user", "content": text},
        ],
        max_tokens=100,
    )

    answer = response["choices"][0]["message"]["content"]

    print(f"The script for given topic is \n \n '{answer}'.")
    return answer
