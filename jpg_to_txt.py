from openai import OpenAI, AzureOpenAI
import base64
import os


client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),  
    api_version=os.getenv("OPENAI_API_VERSION"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
)

# Function to encode the image
def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

# Path to your image
image_path = r"jpgs_to_review\Find_mistakes_1.jpg"

# Getting the base64 string
base64_image = encode_image(image_path)

# Transcription of the text from jpg file that was a pdf before
def jpg_to_text():
    url = f"data:image/jpeg;base64,{base64_image}"
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role":"assistant","content":"Your role is to create a transcription of the text that is on the image."},
            {
            
            "role": "user",
            "content": [
                {"type": "text", "text": "Transcribe the text that is on the image. Do it the best as you can."},
                {
                "type": "image_url",
                "image_url": {
                    "url": url,
                },
                },
            ],
            }
            
        ],
    )
    
    with open("jpg_to_txt.txt", "w") as f:
        f.write(response.choices[0].message.content)

jpg_to_text()