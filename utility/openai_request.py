import openai
import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.getcwd(), ".env")
load_dotenv(dotenv_path)


def request_script(text):
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

def request_image_descriptions(narration):
    prompt= f"""
        I want you to act as the one who can provide me with the Image Description which I can give to image generation tool like midJourney, Stable diffusion etc.

        I will be giving you a text. This text will be a part of narration for a video, I want the most relevant image to be there when the specific text is being narrated.  Pick out the keywords or situation which is the most relevant and create an image description text for it.

        For example: "Welcome to today's videos, where we'll explore 15 psychological facts that will blow your mind. Let's dive right in"

        Here I would want to an image of brain in the background as that will make the most sense

        So now I want you to give me the image description for the below text:

        "{narration}"

        Please give me the output in a single small paragraph or a sentence. This description is what I will give to midjourney for example. 

        Please strictly follow the below format, do not include anything else in the output. You need to provide what is asked in the square bracket below

        Image Description: [exact text to send to image generation tool]
    """

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=100
    )

    image_description = response["choices"][0]["message"]["content"]

    print(f"The script for given topic is \n \n '{image_description}'.")
    return image_description