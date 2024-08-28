from pdf2image import convert_from_path
from PIL import Image
import time
import os

# Function to convert PDF to JPG images in memory
def pdf_to_images(pdf_path):
    # Start the timer to measure CPU processing time
    start_time = time.process_time()

    # Convert PDF to list of images
    images = convert_from_path(pdf_path)

    # Stop the timer
    end_time = time.process_time()
    
    # Calculate the elapsed CPU time
    elapsed_time = end_time - start_time
    return images, elapsed_time

# Function to combine images vertically
def combine_images_vertically(images, output_path):
    # Start the timer to measure CPU processing time
    start_time = time.process_time()

    # Get the width of the widest image and the total height of all images combined
    total_width = max(img.width for img in images)
    total_height = sum(img.height for img in images)

    # Create a new blank image with the calculated total dimensions
    combined_image = Image.new('RGB', (total_width, total_height))

    # Set initial height to start placing images
    y_offset = 0

    # Paste each image onto the new blank image, one below the other
    for img in images:
        combined_image.paste(img, (0, y_offset))
        y_offset += img.height

    # Save the combined image to the specified output path
    combined_image.save(output_path)

    # Stop the timer
    end_time = time.process_time()
    
    # Calculate the elapsed CPU time
    elapsed_time = end_time - start_time
    return elapsed_time

"""
Easily change the number of the document to change it into jpg.
"""
# User-defined variable
n = 3

# Paths based on user-defined 'n'
pdf_path = f'documents_pdf\\document_{n}.pdf'
output_folder = r'documents_jpg_high_resolution'

# Ensure the output folder exists
os.makedirs(output_folder, exist_ok=True)

# Convert PDF to images
images, pdf_conversion_time = pdf_to_images(pdf_path)

# Combine images into a single image
output_image_path = os.path.join(output_folder, f'document_{n}.jpg')
image_combination_time = combine_images_vertically(images, output_image_path)

# Calculate and print the total processing time
total_processing_time = pdf_conversion_time + image_combination_time
print(f"Total processing time (PDF conversion + image combination): {total_processing_time} seconds")