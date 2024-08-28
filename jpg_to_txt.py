from openai import OpenAI, AzureOpenAI
import base64
import time
import os

os.environ['AZURE_OPENAI_API_KEY'] = 'Put Your OpenAI API Key here'
os.environ['AZURE_OPENAI_ENDPOINT'] = 'Put your OpenAI endpoint here'
os.environ['OPENAI_API_VERSION'] = "Put your OpenAI API version here"

client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),  
    api_version=os.getenv("OPENAI_API_VERSION"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
)

# Transcription of the text from jpg file that was a pdf before
def jpg_to_text(input_image_path, output_text_path):

    # Start the timer to measure CPU processing time
    start_time = time.process_time()

    # Function to encode the image
    def encode_image(image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    # Getting the base64 string from the initial image
    base64_image = encode_image(input_image_path)

    url = f"data:image/jpeg;base64,{base64_image}"
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role":"assistant","content":"Your role is to create a transcription of the text that is on the image."},
            {
            
            "role": "user",
            "content": [
                {"type": "text", "text": """Transcribe the text that is on the image. Do it the best as you can. 
                                            Do not add any additional text before or after transcription."""},
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
    
    with open(output_text_path, "w") as f:
        f.write(response.choices[0].message.content)

    # Stop the timer
    end_time = time.process_time()
    
    # Calculate the elapsed CPU time
    elapsed_time = end_time - start_time
    return elapsed_time


"""
Easily change the number of the document to change it into text file. 
Remember to set if you are interested in high or low resolution images.
"""
doc_number = 3
high_or_low = "low"

input_image_path = f'documents_jpg_{high_or_low}_resolution\\document_{doc_number}.jpg'
output_text_path = f'documents_text_{high_or_low}_resolution\\document_{doc_number}.txt'
print("Time needed to convert pdf into jpg: " + str(jpg_to_text(input_image_path, output_text_path)) + " seconds")