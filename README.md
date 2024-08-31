# Image-vs-text---complete-research

This repository is made to research the problem of using text and image inputs for GPT-4o. There are plenty of algorithms created to get the same input as a text and as an image. Then both outputs can be compared.

**Files explanation**

documents_pdf - is a folder that contains examples of pdfs for the reviewing purpose.

**pdf_to_jpg.py** - Algorithm that changes pdf file into an image by using pdf2immage library. It is needed to run this algorithm before running image review. Outputs are saved in documents_jpg_high_resolution folder

**compress_jpg.py** - Algorithm that compresses images from documents_jpg_high_resolution folder and saves them in documents_jpg_low_resolution folder. The resolution of each image is changed to the 10% of the original image.

**jpg_to_txt.py** - Algorithm that uses GPT-4o to convert image into text. Images were fistly created by pdf_to_jpg.py algorithm. Texts are saved in documents_text_high_resolution and documents_text_low_resolution folders, depending of the resolution of the image used for transcription.

**text_review** - Folder that contains 2 types of algorithms and their outputs. First algorithm conduct (5 times) grammatical review with the text (from pdf) as an input and the outputs are saved in gram_review folder. Second algorithm conduct (5 times) non-promotional review with the text (from pdf) as an input and the outputs are saved in non-prom_review folder.

**image_review_high_resolution** - Folder that contains 2 types of algorithms and their outputs. First algorithm conduct (5 times) grammatical review with the high-resolution image (of pdf) as an input and the outputs are saved in gram_review folder. Second algorithm conduct (5 times) non-promotional review with the high-resolution image (of pdf) as an input and the outputs are saved in non-prom_review folder.

**image_review_low_resolution** - Folder that contains 2 types of algorithms and their outputs. First algorithm conduct (5 times) grammatical review with the low-resolution image (of pdf) as an input and the outputs are saved in gram_review folder. Second algorithm conduct (5 times) non-promotional review with the low-resolution image (of pdf) as an input and the outputs are saved in non-prom_review folder.

**image_text_review** - Folder that contains 2 types of algorithms and their outputs. First algorithm conduct (5 times) grammatical review by firstly doing a text review (of pdf) and then low-resolution image (of pdf) review, that are later comboned by a 3rd prompt to one, better review. The outputs are saved in gram_review folder. Second algorithm conduct (5 times) non-promotional review by firstly doing a text review (of pdf) and then low-resolution image (of pdf) review, that are later comboned by a 3rd prompt to one, better review. The outputs are saved in non-prom_review folder.

All of the needed things to run the algorithm are already inside each file.
Simply, just add a key for OpenAI API to run the algorithm with the use of GPT-4o.