# Python 3.11.6 64-bit
# IMAGE GENERATE & RUN
from PIL import Image
from io import BytesIO
import os, openai, requests
from colorama import Fore

def generate(key, prompt):
    """Generates an image using openai's image api

    Args:
        key (string): open ai api key
        prompt (string): image description
    """
    print(Fore.LIGHTCYAN_EX + "CREATING IMAGE")
    openai.api_key = key
    url = openai.Image.create(
    prompt=prompt,
    n=1,
    size="1024x1024"
    )
    return(url["data"][0]["url"])
    

def show(url):
    """Retrieves, downloads, and opens image from URL

    Args:
        url (string): url of image
    """
    response = requests.get(url, verify=False)
    os.system('cls')
    print(Fore.LIGHTCYAN_EX + "OPENING IMAGE")
    if response.status_code == 200:
        content_type = response.headers['content-type']
        if 'image' in content_type:
            image = Image.open(BytesIO(response.content))
            image.save("temp.jpg")
            os.startfile("temp.jpg")
        else:
            print("The URL does not point to an image.")
    else:
        print("Failed to retrieve data from the URL.")

def main(prompt, key):
    print(Fore.LIGHTCYAN_EX + "IMAGE IDENTIFIED")
    url = generate(key, prompt)
    show(url)

if __name__ == "__main__":
    main('key_here', input("DEBUG: "))
