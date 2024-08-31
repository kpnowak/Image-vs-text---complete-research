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

#### 
####  Put a number of the document that you are interested in.
####

doc_num = 2

with open(f'documents_text_high_resolution\\document_{doc_num}.txt', 'r', encoding='latin-1') as file:
    jpg_to_txt_content = file.read()

# Function to encode the image
def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

# Path to your image
image_path = f"documents_jpg_low_resolution\\document_{doc_num}.jpg"
# Getting the base64 string
base64_image = encode_image(image_path)

NON_PROMOTIONAL_GUIDELINES = """
Source - EFPIA Chapter 3:
Article 16 - Lifelong Learning in Healthcare
    i. Lifelong learning in healthcare (LLH) is aimed at increasing the scientific knowledge and competence of HCPs to enhance medical practice and improve patient outcome. Member Companies can be engaged in or support different types of educational programs but such activities must not constitute Promotion. These activities can be one of three types: a) Independent Medical Education i.e. conducted by an independent organisation and funded by the industry; b) programs that are developed in collaboration with another stakeholder; or c) pharmaceutical industry led LLH activities. When funding Independent Medical Education or organizing LLH activities directly or in collaboration with third parties, Member Companies must ensure that their participation and role is clearly acknowledged and apparent from the outset. LLH activities must have content that is fair, balanced and objective, designed to allow the expression of diverse evidence-based science and fulfill unmet educational needs in healthcare. This Article is complemented by a Guideline on a Quality Framework for LLH (Annex 3)."
Article 17 - Informational or Educational Materials and Items of Medical Utility
    i. The provision of Informational or Educational Materials is permitted provided it is: (a) “inexpensive”; (b) directly relevant to the practice of medicine or pharmacy; and (c) directly beneficial to the care of patients."
    ii. Items of Medical Utility aimed directly at the education of HCPs and patient care can be provided if they are “inexpensive” and do not offset routine business practices of those who receive them."
    iii. The nature of Informational or Educational Materials and Items of Medical Utility considered may not constitute a circumvention of the prohibition on gifts defined under Article 11 of this Code. The transmission of such materials or items must not constitute an inducement to recommend and/or prescribe, purchase, supply, sell or administer a Medicinal Product."
    iv. Informational or Educational Materials and Items of Medical Utility can include the Member Company name, but must not be product branded, unless the Medicinal Product’s name is essential for the correct use of the material or item by the patient."
Article 18 - Non-Interventional Studies
    i. Non-Interventional Studies must be conducted with a primarily scientific purpose and must not be disguised Promotion."
    ii. Non-Interventional Studies that are prospective in nature and that involve the collection of patient data from or on behalf of individual, or groups of, HCPs specifically for the study must comply with all of the following criteria: There is a written study plan (observational plan/protocol); In countries where ethics committees are prepared to review such studies, the study plan must be submitted to the ethics committee for review; The study plan must be approved by the Member Company’s scientific service and the conduct of the study must be supervised by the Member Company’s scientific service as described in Section 20.01.a; The study results must be analysed by or on behalf of the contracting Member Company and summaries thereof must be made available within a reasonable period of time to the Member Company’s scientific service (as described in Section 20.01.a), which service must maintain records of such reports for a reasonable period of time. The Member Company must send the summary report to all HCPs that participated in the study and must make the summary report available to industry self-regulatory bodies and/or committees that are in charge of supervising or enforcing Applicable Codes upon their request. If the study shows results that are important for the assessment of benefit-risk, the summary report must be immediately forwarded to the relevant competent authority; and Medical Sales Representatives may only be involved in an administrative capacity and such involvement must be under the supervision of the Member Company’s scientific service that will also ensure that the Medical Sales Representatives are adequately trained. Such involvement must not be linked to the Promotion of any Medicinal Product."
    iii. To the extent applicable, Member Companies are encouraged to comply with Section 18.02 for all other types of NIS, including epidemiological studies and registries and other studies that are retrospective in nature. In any case, such studies are subject to Article 15.01."
Article 19 - Medical Samples
    i. In principle, no Medical Samples should be given, except on an exceptional basis. Medical Samples must not be given as an inducement to recommend and/or prescribe, purchase, supply, sell or administer specific Medicinal Products, and must not be given for the sole purpose of treating patients. Medical Samples are provided to HCPs so that they may familiarise themselves with the Medicinal Product and acquire experience in dealing with them. In accordance with national and/or EU laws and regulations, a limited number of Medical Samples may be supplied on an exceptional basis and for a limited period. A reasonable interpretation of this provision is that each HCP should receive, per year, not more than 4 Medical Samples of a particular Medicinal Product he/she is qualified to prescribe for 2 years after the HCP first requested samples of each particular Medicinal Product (i.e. the “4x2” standard). In this context, a new Medicinal Product is a product for which a new marketing authorisation has been granted, either following an initial marketing authorisation application or following an extension application for new strengths/dosage forms that include a new indication. Extensions of the marketing authorisation to additional strengths/dosage forms for existing indications or pack sizes (number of units in the pack) cannot be considered as new Medicinal Product. Without prejudice to the ban on medical sampling of Medicinal Product containing psychotropic and narcotic substances, Medical Samples can only be given in response to a written request from HCPs qualified to prescribe that particular Medicinal Product. Written requests must be signed and dated by those who ask for the Medical Samples. On an exceptional basis, Member Associations may allow, through additional guidance, a longer period than 2 years if required by local healthcare conditions."
    ii. Member Companies must have adequate systems of control and accountability for Medical Samples which they distribute and for all Medicinal Products handled by theirs Medical Sales Representatives. This system must also clearly establish, for each HCP, the number of Medical Samples supplied in application of the provisions in Section 19.01."
    iii. Each Medical Sample must be no larger than the smallest presentation of that particular Medicinal Product in the relevant country. Each Medical Sample must be marked “free medical sample – not for sale” or words to that effect and must be accompanied by a copy of the summary of product characteristics."
Article 20 - Member Company Staff
    i. All Member Company staff must be fully conversant with the relevant requirements of the Applicable Code(s) and laws and regulations. Each Member Company must establish a scientific service in charge of information about its Medicinal Products and the approval and supervision of NIS. Member Companies are free to decide how best to establish such service(s) in accordance with this Section 20.01 (i.e. whether there is one service in charge of both duties or separate services with clearly delineated duties), taking into account their own resources and organisation. The scientific service must include a medical doctor or, where appropriate, a pharmacist who will be responsible for approving any promotional material before release. Such person must certify that he or she has examined the final form of the promotional material and that in his or her belief it is in accordance with the requirements of the Applicable Code(s) and any relevant laws and regulations, is consistent with the summary of product characteristics and is a fair and truthful presentation of the facts about the Medicinal Product. In addition, the scientific service must include a medical doctor or, where appropriate, a pharmacist, who will be responsible for the oversight of any NIS (including the review of any responsibilities relating to such studies, particularly with respect to any responsibilities assumed by Medical Sales Representatives). Such person must certify that he or she has examined the protocol relating to the NIS and that in his or her belief it is in accordance with the requirements of the Applicable Code(s) and any relevant laws and regulations. Each Member Company must appoint at least one senior employee who must be responsible for supervising the Member Company and its subsidiaries to ensure that the standards of the Applicable Code(s) are met."
    ii. Each Member Company must ensure that its Medical Sales Representatives are familiar with the relevant requirements of the Applicable Code(s), and all applicable laws and regulations, and are adequately trained and have sufficient scientific knowledge to be able to provide precise and complete information about the Medicinal Products they promote. Medical Sales Representatives must comply with all relevant requirements of the Applicable Code(s), and all applicable laws and regulations, and Member Companies are responsible for ensuring their compliance. Medical Sales Representatives must approach their duties responsibly and ethically. During each visit, and subject to applicable laws and regulations, Medical Sales Representatives must give the persons visited, or have available for them, a summary of the product characteristics for each Medicinal Product they present. Medical Sales Representatives must transmit to the scientific service of their companies forthwith any information they receive in relation to the use of their company’s Medicinal Products, particularly reports of side effects. Medical Sales Representatives must ensure that the frequency, timing and duration of visits to HCPs, pharmacies, hospitals or other healthcare facilities, together with the manner in which they are made, do not cause inconvenience. Medical Sales Representatives must not use any inducement or subterfuge to gain an interview. In an interview, or when seeking an appointment for an interview, Medical Sales Representatives must, from the outset, take reasonable steps to ensure that they do not mislead as to their identity or that of the Member Company they represent."

Source - EFPIA Chapter 4:
Article 21 - Interactions with POs
    i. Member Companies must comply with the following principles that EFPIA, together with pan-European POs, have subscribed to: The independence of POs, in terms of their political judgement, policies and activities, must be assured. All interactions between POs and Member Companies must be based on mutual respect, with the views and decisions of each partner having equal value. Member Companies must not request, nor shall POs undertake, the Promotion of a particular POM. The objectives and scope of any collaboration must be transparent. Financial and non-financial support provided by Member Companies must always be clearly acknowledged. Member Companies welcome broad funding of POs from multiple sources."
    ii. EU and national laws and regulations prohibit the advertising of POM to the general public."
    iii. When Member Companies provide financial support, significant indirect support and/or significant non-financial support to POs, they must have in place a written agreement. This must state the amount of funding and also the purpose (e.g. unrestricted grant, specific meeting or publication, etc). It must also include a description of significant indirect support (e.g. the donation of public relations agency´s time and the nature of its involvement) and significant non-financial support."
    iv. Member Companies must not influence the text of PO’s material they sponsor in a manner favourable to their own commercial interests. This does not preclude Member Companies from correcting factual inaccuracies. In addition, at the request of POs, Member Companies may contribute to the drafting of the text from a fair and balanced scientific perspective."

Source - Communicate With Care Pocket Guide: 
Article 1 - Be Mindful
    i. Consider Legal Implications: Remember that written communications may become evidence in legal matters. 
    ii. Assess Document Sensitivity: Evaluate if the content should be shared or discussed in a less permanent form, like verbally. 
Article 2 - Be Clear and Professional 
    i. Maintain Professional Tone: Use polite language, avoid sarcasm and humor. 
    ii. Provide Context: Ensure clarity to prevent misunderstandings, especially for those unfamiliar with the topic. 
    iii. Stick to Facts: Avoid exaggerations and speculations. 
Article 3 - Do Not Ignore Inappropriate Writing
    i. Address Concerns: If you encounter inappropriate content, seek clarification or involve Legal/Compliance.

Source - Disclaimer Texts for Non-promotional Material:
Article 1 - Internal Communication: 
    i. Use: “This material is for preparatory use in NN only.” 
    ii. When: Regarding promotional or non-promotional material (e.g., strategies, plans, internal launch communication, Q&As, training material, internal PowerPoint presentations). 
    iii.Note: Add “DRAFT” if not final and/or “CONFIDENTIAL” if required. 
Article 2 - Draft Non-Promotional Material: 
    i. Use: “This is a DRAFT, for preparatory use in NN only. Affiliates are responsible for compliance with local procedures and for review of such non-promotional material, e.g., against more stringent local legislation, and if relevant local code of conduct before distribution.” 
    ii. When: Sent to affiliates for local adaptation and distribution externally (e.g., disease awareness, press releases). 
Article 3 - General Disclaimers include in all pages: 
    i. “The image shown is a model and not a real patient.” 
    ii. “The prescription is based on a patient example and not a real patient.” 
    iii. “Model is not a real patient and situations shown do not reflect models’ experience.” 
    iv. “The character and its description are for representation purposes only and does not reflect real patient.” 
    v. “This information is intended for diabetes patients who have been prescribed [insert NN medicinal product] and should not be substituted for medical advice from your doctor.” 
    vi. “Please see patient information leaflet in the package for additional information.” 
    vii. “If you experience any side effects while using [insert NN medicinal product], talk to your doctor, pharmacist or nurse. This includes any possible side effects not listed in the package leaflet. You can also report side effects directly via [insert the local customer contact function or local safety department].”

Source - Global Legal & Compliance Pocket Guide Semaglutide portfolio Appropriate product communication:
Article 1 - Non-Promotional Material: 
    i. Scientific Information Exchange: Sharing of scientific information about products is allowed to keep the medical community informed about new developments and product safety. This includes sharing off-label information in a balanced and objective way to an appropriate audience. 
    ii. Off-Label Information: Dissemination of factual information about unapproved products or new clinical data is permitted without promotional intent, provided it’s communicated in the right context. Off-label promotion, however, is strictly prohibited. 
"""

# ------------------------------------------------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------- TEXT -------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------------------------------------

non_promotional_material_prompt_template_txt = f"""

You as an expert reviewer for promotional materials, your role is to meticulously review non-promotional materials in accordance with "Non-Promotional Material Guidelines". It is imperative to follow the instructions provided and ensure your response meets the required standards. 

"Promotional Material Guidelines" delimited by XXX: 
XXX 
{NON_PROMOTIONAL_GUIDELINES} 
XXX 

Please review the following document using the "Non-Promotional Material Guidelines" provided above. The document to review is delimited by XXX below: 
XXX 
{jpg_to_txt_content}
XXX 
    
You should start your review by studying the "Non-Promotional Material Guidelines", remember to adhere to the ethical principles outlined in the document and maintain high standards when reviewing materials. Each point should be carefully checked to ensure compliance with the "Non-Promotional Material Guidelines". 

Please provide the following response for each of your new sentences:
- Guideline source which influenced your response
- The source sentence your new sentence replaces 
- The deviations your new sentence corrects
- In the deviations write which source and key point from "Non-Promotional Material Guidelines" influenced the response (i.e. "According to [Source - Communicate With Care Pocket Guide] the information suggests that [write your deviations here])
- Your new sentence 
- The reason for replacing the source sentence with your new sentence and how it resolves the referenced deviations 
   
Try to correct as many deviations as you can. 
    
Double-check your working, ensuring that you've considered the entire document provided and your comments refer clearly to the Non-Promotional Material Guidelines. 
   
Do not provide duplicate comments. No two comments in your response should be the same. If there are any duplicate comments, remove them from your response, keeping the original. 
"""

# -------------------------------------------------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------- PHOTO --------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------------------------------------------------------------------

non_promotional_material_prompt_template_jpg = f"""

You as an expert reviewer for promotional materials, your role is to meticulously review non-promotional materials in accordance with "Non-Promotional Material Guidelines". It is imperative to follow the instructions provided and ensure your response meets the required standards. 

"Non-Promotional Material Guidelines" delimited by XXX: 
XXX 
{NON_PROMOTIONAL_GUIDELINES} 
XXX 

Please review the image that you are provided with, which is the document, by using the "Non-Promotional Material Guidelines" provided above. The document to review is the image.
    
You should start your review by studying the "Non-Promotional Material Guidelines", remember to adhere to the ethical principles outlined in the document and maintain high standards when reviewing materials. Each point should be carefully checked to ensure compliance with the "Non-Promotional Material Guidelines". 

Please provide the following response for each of your new sentences:
- Guideline source which influenced your response
- The source sentence your new sentence replaces 
- The deviations your new sentence corrects
- In the deviations write which source and key point from "Non-Promotional Material Guidelines" influenced the response (i.e. "According to [Source - Communicate With Care Pocket Guide] the information suggests that [write your deviations here])
- Your new sentence 
- The reason for replacing the source sentence with your new sentence and how it resolves the referenced deviations 
   
Try to correct as many deviations as you can. 
    
Double-check your working, ensuring that you've considered the entire document provided and your comments refer clearly to the Non-Promotional Material Guidelines. 
   
Do not provide duplicate comments. No two comments in your response should be the same. If there are any duplicate comments, remove them from your response, keeping the original. 
"""

# ------------------------------------------------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------- TEXT -------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------------------------------------

def text_review():

    # Start the timer to measure CPU processing time
    start_time = time.time()

    # first review code
    response1 = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that reviews the documents."},
            {"role": "user", "content": f"{non_promotional_material_prompt_template_txt}"},
        ]
    )

    # chef review instruction
    final_non_promotional_review_prompt_template_txt = f"""
    You are the chief reviewer for reviews performed for "Non-Promotional Material Guidelines". You are provided with document reviews from your team of expert reviewers. You are responsible for checking over their reviews and providing feedback to the reviewers before publishing the reviews to the client. 

    Below are the guidelines for the "Non-Promotional Material Guidelines" delimited by XXX: 
    XXX 
    {NON_PROMOTIONAL_GUIDELINES} 
    XXX 
   
    Please conduct a review upon the Expert's comments below delimited by XXX: 
    XXX 
    {response1.choices[0].message.content}
    XXX 
    
    Work through each of the comments provided by the expert reviewer. You should start by understanding "Non-Promotional Material Guidelines" guidelines. Next you should verify that the expert's suggested change adheres to every single one of the guidelines. If there can be an improvement to the expert's suggested change or is inadequate with regards to the "Non-Promotional Material Guidelines", please create a new suggested change which better adhere's to all of the guidelines, this can be a completely new sentence if needed. 
    
    Please provide the following response for each of the comments you've improved upon: 
        - The original source sentence
        - The deviation from the guidelines originally provided by the expert reviewer
        - The expert reviewer's original suggested change 
        - An explanation for the reason behind your new suggested change 
        - Your new suggested sentence
        - In the deviations write which source and key point from "Non-Promotional Material Guidelines" influenced the response (i.e. "According to [Source - Communicate With Care Pocket Guide] the information suggests that [write your deviations here])
    
    Comments which you have not improved upon can be left out of your response 
    
    In your review you should make sure that your suggested changes are not just copies of the source sentence nor a copy of the expert reviewer's sentence and they adhere to the guidelines 
    
    Take your time to work through the comments systematically in a step-by-step process. 
 
    Double check that you've examined every comment provided by the expert reviewer, if there are any you missed on your initial check, please go back and review them in the same manner as previously defined. If a suggestion by the expert reviewer is correct and adheres to the guidelines, you should skip it and do not mention it in your response. 
    Be careful, because this text will be saved as txt file, so do NOT use any weird characters. Just do a plain text. Don't use character '\x97'. It is very important so be careful. You cannot provoke this error in Python 'UnicodeEncodeError: 'charmap' codec can't encode character '\x97' in position 5210: character maps to <undefined>'.
    """

    # chef review code
    response2 = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that reviews the documents."},
            {"role": "user", "content": f"{final_non_promotional_review_prompt_template_txt}"},
        ]
    )

    # Separator and header
    separator = "-" * 94
    header = "-" * 40 + " Chief Output " + "-" * 40

    merged_content = f"{response1.choices[0].message.content}\n\n{separator}\n{header}\n{separator}\n\n{response2.choices[0].message.content}"

    # Stop the timer
    end_time = time.time()

    # Calculate the elapsed CPU time
    elapsed_time = end_time - start_time

    return merged_content, elapsed_time

# -------------------------------------------------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------- PHOTO --------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------------------------------------------------------------------

def jpg_review():

    # Start the timer to measure CPU processing time
    start_time = time.time()

    url = f"data:image/jpeg;base64,{base64_image}"
    response1 = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role":"assistant","content":"Your role is to review an image, which is a document."},
            {
            
            "role": "user",
            "content": [
                {"type": "text", "text": f"{non_promotional_material_prompt_template_jpg}"},
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
    
    # chef review instruction
    final_non_promotional_review_prompt_template_jpg = f"""
    You are the chief reviewer for reviews performed for "Non-Promotional Material Guidelines". You are provided with document reviews from your team of expert reviewers. You are responsible for checking over their reviews and providing feedback to the reviewers before publishing the reviews to the client. 

    Below are the guidelines for the "Non-Promotional Material Guidelines" delimited by XXX: 
    XXX 
    {NON_PROMOTIONAL_GUIDELINES} 
    XXX 
   
    You are provided with an image of the document that your team of experts already reviewed.
    Please conduct a review upon the image of the document that you are provided with and the Expert's comments below delimited by XXX:
    XXX 
    {response1.choices[0].message.content}
    XXX 
    
    Work through each of the comments provided by the expert reviewer. You should start by understanding "Non-Promotional Material Guidelines" guidelines. Next you should verify that the expert's suggested change adheres to every single one of the guidelines. If there can be an improvement to the expert's suggested change or is inadequate with regards to the "Non-Promotional Material Guidelines", please create a new suggested change which better adhere's to all of the guidelines, this can be a completely new sentence if needed. 
    
    Please provide the following response for each of the comments you've improved upon: 
        - The original source sentence
        - The deviation from the guidelines originally provided by the expert reviewer
        - The expert reviewer's original suggested change 
        - An explanation for the reason behind your new suggested change 
        - Your new suggested sentence
        - In the deviations write which source and key point from "Non-Promotional Material Guidelines" influenced the response (i.e. "According to [Source - Communicate With Care Pocket Guide] the information suggests that [write your deviations here])
    
    Comments which you have not improved upon can be left out of your response 
    
    In your review you should make sure that your suggested changes are not just copies of the source sentence nor a copy of the expert reviewer's sentence and they adhere to the guidelines 
    
    Take your time to work through the comments systematically in a step-by-step process. 
 
    Double check that you've examined every comment provided by the expert reviewer, if there are any you missed on your initial check, please go back and review them in the same manner as previously defined. If a suggestion by the expert reviewer is correct and adheres to the guidelines, you should skip it and do not mention it in your response. 
    Be careful, because this text will be saved as txt file, so do NOT use any weird characters. Just do a plain text.
    """

    url = f"data:image/jpeg;base64,{base64_image}"
    response2 = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role":"assistant","content":"Your role is to review an image."},
            {
            
            "role": "user",
            "content": [
                {"type": "text", "text": f"{final_non_promotional_review_prompt_template_jpg}"},
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

    # Separator and header
    separator = "-" * 94
    header = "-" * 40 + " Chief Output " + "-" * 40

    merged_content = f"{response1.choices[0].message.content}\n\n{separator}\n{header}\n{separator}\n\n{response2.choices[0].message.content}"

    # Stop the timer
    end_time = time.time()

    # Calculate the elapsed CPU time
    elapsed_time = end_time - start_time

    return merged_content, elapsed_time

# ------------------------------------------------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------- COMBINED ----------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------------------------------------

text, time_text = text_review()
image, time_image = jpg_review()

only_text = f"""
There are two reviews done of the same text. You need to combine both of these reviews to create one the best review on earth that will contain information from both of them.
These reviews are done with the use of different output, but both of them are about the same non-promotional review.

To make it easier for creating the best review in the world, you should see the initial text that is being reviewed, which is below and delimited by XXX:
XXX 
{jpg_to_txt_content} 
XXX

Now let's create the best review in the world that will combine these two reviews.

Belowe is Review 1 delimited by XXX:
XXX
{text}
XXX

Belowe is Review 2 delimited by XXX:
XXX
{image}
XXX
"""

both_text_and_image = f"""
There are two reviews done of the same text. You need to combine both of these reviews to create one 
the best review on earth that will contain information from both of them.
These reviews are done with the use of different output, but both of them are about the same 
non-promotional review.

To make it easier for creating the best review in the world, you should see the initial text that is 
being reviewed, which is an image inputed with this message.

Now let's create the best review in the world that will combine these two reviews.

Belowe is Review 1 delimited by XXX:
XXX
{text}
XXX

Belowe is Review 2 delimited by XXX:
XXX
{image}
XXX
"""

def both_review_only_txt_5():
    for i in range(5):
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that combines reviews to make them better."},
                {"role": "user", "content": f"{only_text}"},
            ]
        )
        with open(f"image_text_review\\non-prom_review\\document_{doc_num}_output_only_text{i+1}.txt", "w") as f:
            f.write(response.choices[0].message.content)

def both_review_with_image_5():

    # Start the timer to measure CPU processing time
    start_time = time.time()

    for i in range(5):
        url = f"data:image/jpeg;base64,{base64_image}"
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role":"assistant","content":"""You are a helpful assistant that 
                                                combines reviews to make them better."""},
                {
                
                "role": "user",
                "content": [
                    {"type": "text", "text": f"{both_text_and_image}"},
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
        
        with open(f"image_text_review\\non-prom_review\\document_{doc_num}_output_with_image{i+1}.txt", "w") as f:
            f.write(response.choices[0].message.content)
    
    # Stop the timer
    end_time = time.time()

    # Calculate the elapsed CPU time
    elapsed_time = end_time - start_time

    return elapsed_time



time_combine = both_review_with_image_5()

per_one_combine = time_combine / 5

total_time = time_image + time_text + per_one_combine

print(f"Total time of running: {total_time:.6f} seconds")