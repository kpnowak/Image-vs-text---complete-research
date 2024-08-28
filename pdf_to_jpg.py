from pdf2image import convert_from_path
import os

# Function to convert PDF to JPG
def pdf_to_jpg(pdf_path, output_folder, n):
    # Convert PDF to list of images
    images = convert_from_path(pdf_path)

    # Iterate through the images and save each one as a JPG file
    for i, image in enumerate(images):
        image_path = os.path.join(output_folder, f'document_{n}page_{i + 1}.jpg')
        image.save(image_path, 'JPEG')
        print(f'Saved: {image_path}')

"""
To change the document that you want to convert from PDF to JPG, simply change 'n' to appropiate number of the document.
"""
n = 2
pdf_path = f'documents_pdf\\document_{n}.pdf'
output_folder = r'documents_jpg'

# Ensure the output folder exists
os.makedirs(output_folder, exist_ok=True)

pdf_to_jpg(pdf_path, output_folder, n)