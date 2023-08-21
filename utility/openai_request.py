import openai
import os
import re
from dotenv import load_dotenv

# load_dotenv()
def refresh_env():
    load_dotenv(override=True)
    openai.api_key = os.getenv('OPENAI_SECRET_KEY')
    openai.organization = os.getenv('OPENAI_ORG')

# openai.api_key = refresh_env('OPENAI_SECRET_KEY')
# openai.organization = refresh_env('OPENAI_ORG')

def extract_narration(text):
    # The pattern looks for 'Narrator:' followed by any character (.) zero or more times (?)
    # until a double-quote is found. The non-greedy modifier '?' ensures we capture the shortest match.
    pattern = r'Narrator: ".*?"'
    
    matches = re.findall(pattern, text)
    return '\n\n'.join(matches)


def request_script(text):
    refresh_env()
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "user",
                "content": f"""I am providing you the title of the video: "{text}". I want you to create a video script in the format I provide below. The script should be divided into narration speech which will be spoken in the video. Below is the format where each narration should start with "Narrator:" and then the actual speech to be spoken in the video. In the below format it is represented by double quotes. Make sure there is nothing else in the output. There should strictly be only narration speech no image description text or anything else in the output. also do not reply with any other text such as 
                    I'd be happy to help you create the video script. Here it is following the format you provided:, etc etc etc
                    The output should only strictly contain narrator scripts in the specified format.

                    Narrator: "Narration speech 1"
                    Narrator: "Narration speech 2"
                    Narrator: "Narration speech 3"
                    """
            },
        ],
        max_tokens=3500,
    )

    answer = response["choices"][0]["message"]["content"]

    refined_answer = extract_narration(answer)

    print(f"The script for given topic is \n \n '{refined_answer}'.")
    return refined_answer

def request_image_descriptions(narration, title):
    refresh_env()
    prompt= f"""
        I want you to act as the one who can provide me with the Image Description which I can give to image generation tool like midJourney, Stable diffusion etc.

        I will be giving you a text. This text will be a part of narration for a video, I want the most relevant image to be there when the specific text is being narrated.  Pick out the keywords or situation which is the most relevant and create an image description text for it.

        For example: "Welcome to today's videos, where we'll explore 15 psychological facts that will blow your mind. Let's dive right in"

        Here I would want to an image of brain in the background as that will make the most sense

        In addition to that I am also giving you the title of this particular video from whose entire script I am giving you the text.

        This is the title of the video: "{title}". This is just for reference to give you context

        So now I want you to give me the image description for the below text:

        "{narration}"

        Please give me the output in a single small sentence. This description is what I will give to midjourney for example. 

        Please strictly follow the below format, do not include anything else in the output and keep the Image description less than 15 to 20 words. You need to provide what is asked in the square bracket below

        Image Description: [exact text to send to image generation tool]
    """

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=2000
    )

    image_description = response["choices"][0]["message"]["content"]
    pattern = r'Image Description: [\'"]?(.*?)[\'"]?(?=\.$|$)'
    # pattern = r"Image Description: \[(.*?)\]"
    match = re.search(pattern, image_description)
    if match:
        result = match.group(1).strip().replace("  ", " ")
        result = re.sub(r'^[\'"]|[\'"]$', '', result)
        result = re.sub(r'\s+', ' ', result)
        print(f"The script for given topic: \n \n '{result}'.")
        return result
    else:
        print(f"The script for given topic is \n \n '{image_description}'.")
        return image_description

# dotenv_path = os.path.join(os.getcwd(), ".env")