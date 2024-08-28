from PIL import Image
import time
import os

def compress_image(input_image_path, output_image_path, target_ratio=0.1):
    # Start the timer to measure CPU processing time
    start_time = time.process_time()
    
    # Open the image file
    with Image.open(input_image_path) as img:
        # Get the original file size
        original_size = os.path.getsize(input_image_path)
        print(f"Original size: {original_size / 1024:.2f} KB")
        
        # Estimate the quality to achieve target file size
        quality = 95
        while True:
            # Save the image with the current quality
            img.save(output_image_path, "JPEG", quality=quality)
            
            # Check the file size of the compressed image
            compressed_size = os.path.getsize(output_image_path)
            print(f"Compressed size at quality {quality}: {compressed_size / 1024:.2f} KB")
            
            # Check if the compressed image meets the target ratio
            if compressed_size <= original_size * target_ratio:
                break
            else:
                # Reduce the quality for further compression
                quality -= 5
                if quality < 10:  # Avoid quality going too low
                    break
        
        print(f"Final compressed size: {compressed_size / 1024:.2f} KB with quality {quality}")

    # Stop the timer
    end_time = time.process_time()
    
    # Calculate the elapsed CPU time
    return end_time - start_time

"""
Easily change the number of the document to change it into lower resolution.
"""
doc_number = 3

input_image_path = f'documents_jpg_high_resolution\\document_{doc_number}.jpg'
output_image_path = f'documents_jpg_low_resolution\\document_{doc_number}.jpg'
print("Time needed to convert pdf into jpg: " + str(compress_image(input_image_path, output_image_path, target_ratio=0.1)) + " seconds")