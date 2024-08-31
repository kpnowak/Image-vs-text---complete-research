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
####  Put a path to the transcription of the document that you are interested in.
####
with open('documents_text_high_resolution\\document_1.txt', 'r', encoding='latin-1') as file:
    jpg_to_txt_content = file.read()

MULTILANGUAGE_GUIDELINES = """
1. Grammar and Punctuation: 
    i. Correct any grammatical errors, taking into account the specific rules of the language. 
    ii. Fix punctuation mistakes, including commas, periods, semicolons, colons, and quotation marks, according to the standards of the language. Ignore the lack of period at the end of the sentence.
    ii. Ensure correct use of capitalization, especially for proper nouns and at the beginning of sentences.
    iii. Avoid hyphen usage corrections.
2. Sentence Structure: 
    i. Ensure all sentences are complete and properly structured as per the syntax and grammar rules of the language. 
    ii. Reorganize sentences if necessary to improve clarity and readability while preserving the original meaning.
3. Consistency: 
    i. Maintain consistent verb tenses throughout the document, as per the conventions of the language. 
    ii. Ensure consistent use of pronouns, articles, and other language-specific constructs.
    ii. Standardize terminology and style across the document.
4. Spelling: 
    i. Correct any spelling mistakes, considering the spelling rules of the language.
    ii. Do not correct medical terminology. Some components of the text may contain typical medical jargon (such as sentence fragments related to dosage and use). These are not grammatical errors but rather standard formulations in the medical industry.
5. Clarity and Readability: 
    i. Improve the clarity of sentences where needed, considering the nuances and complexities of the language. 
    ii. Simplify complex sentences if they hinder understanding, while respecting the language’s structure and style. 
    iii. Ensure the overall readability of the document, taking into account the reading habits and preferences of speakers of the language.
6. Language-Specific Rules: 
    i. Apply language-specific rules and conventions for Mandarin, French, Dutch, Slovak, etc., as each language has unique characteristics and rules.
    ii. For German, replace "Wenn" with "Als" to indicate a specific event that happened in the past.
    iii. Apply language-specific correct relative pronoun replace the relative pronoun with the one that accurately conveys the relationship based on the verb and preposition used.
    iv. Apply language-specific Correct the Idiomatic Expression ensure the idiomatic expression is used correctly according to standard usage
    v. Ensure reflexive pronouns agree with the verb and are in the correct case (e.g., in German, "mir" instead of "mich" when the verb requires the dative case).
    vi. Capitalize nouns, especially when they can be easily confused with other parts of speech (e.g., "Paar" instead of "paar" when referring to a specific number of items).
7. Formality and Tone:
    i. Assess the overall formality of the document, considering the intended audience and purpose.
    ii. Adapt the language, style, and tone to match the required level of formality. Use formal or informal expressions, vocabulary, and structures as appropriate.
    iii. Numbers can be written numerically or with words. Do not correct.
"""

multi_lang_grammar_review_prompt_template_txt = f"""

You are the expert writing reviewer that specifies in correcting spelling and grammar in [document_language] language.
Your role is to meticulously review a document for grammatical accuracy.
It is imperative to follow the steps and instructions provided and ensure your response meets the required standards.

The extracted text below is a very long string and is the result of an actual medical document that was run through a text extractor. Some of the structure may be missing or hard to identify due to the extraction process. When reviewing, please focus on correcting grammatical issues and avoid making changes related to potential structural problems caused by the extraction process.
The document to review is delimited by XXX below: 
XXX 
{jpg_to_txt_content} 
XXX

Step 1: Carefully identify the prominent language of the document. Pay special attention to local languages that may be similar to more widely spoken languages (for example, Catalan vs Spanish). Once identified, store the specific language of the document in [document_language].
Step 2: If [document_language] == French and English, then [document_language] == English. Skip reviewing any French content
Step 2: If [document_language] == zh, then [document_language] == zh_TW.
Step 3: If [document_language] != English then translate the prompt below in [document_language] language:
Step 4: Study the prompt and "Grammar & Spelling Guidelines", "IMPORTANT CONSIDERATIONS WHILE REVIEWING". 
Step 5: Work through each sentence, one at a time. Only review, strictly, sentences in [document_language] language. Never translate anything.
Step 6: Provide reviews and corrections for each sentence that meets the criteria. Only sentences in [document_language] language

"Grammar & Spelling Guidelines" delimited by XXX below: 
XXX 
{MULTILANGUAGE_GUIDELINES}
XXX

IMPORTANT CONSIDERATIONS WHILE REVIEWING:
1. THINGS YOU MUST FOLLOW:
    i. Some components of the text may contain typical medical jargon (such as sentence fragments related to dosage and use). These are not grammatical errors but rather standard formulations in the medical industry.
    ii. Double-check your working, ensuring that you have considered the entire document provided and your comments refer clearly to the "Grammar & Spelling Guidelines". 
    iii. Evaluate the difference between the source sentence and the suggested sentence. Make sure they are not the same. Remove the review if they are
    iv. When reviewing English sentences, please do so according to British English.
    v. Try to correct as many deviations as you can.
2. THINGS YOU MUST AVOID:
    i. AVOID providing a response or a review when skipping the review due to French content identified in English content
    ii. AVOID suggesting translating document sentences to maintain consistency. You are correcting grammar in [document_language] language not translating document content!
    iii. AVOID providing a response for URLs, file names, formulas, citations, slogans, logos, references, HTML format.
    iv. AVOID suggesting to add a period at the end of sentences.
    v. AVOID suggesting a review when there is no grammatical error or deviation noted.
    vi. AVOID suggesting reviewing hyphens/dashes formatting.
    vii. AVOID suggesting reviewing citation formatting.
    viii. AVOID reviewieving medical compounds.
    ix. AVOID providing duplicate comments. No two comments in your response should be the same. If there are any duplicate comments, remove them from your response, keeping the original.
    x. AVOID providing a review when there are no grammatical error or deviation noted in a sentence.
    xi. AVOID providing a response if you DO NOT find any relevant issue with the sentence being reviewed.

Please provide the following response for each of the comments you've improved upon: 
- The source sentence your new sentence replaces
- The deviations your new sentence corrects.
- The reason for replacing the source sentence with your new sentence and how it resolves the referenced deviations.
- Your new sentence

Remember that this review needs to be saved by Python algorithm to txt file, so avoid this error: "UnicodeEncodeError: 'charmap' codec can't encode character '\x97' in position 1349: character maps to <undefined>"
"""

def combiner(response1, response2):
    # Separator and header
    separator = "-" * 94
    header = "-" * 40 + " Chief Output " + "-" * 40

    # Prepare the merged content
    merged_content = f"{response1}\n\n{separator}\n{header}\n{separator}\n\n{response2}"

    return merged_content


def text_review_5():
    for i in range(5):
        # Start the timer to measure CPU processing time
        start_time = time.time()

        # first review code
        response1 = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that reviews the documents."},
                {"role": "user", "content": f"{multi_lang_grammar_review_prompt_template_txt}"},
            ]
        )

        # chef review instruction
        chief_multi_lang_grammar_review_prompt_template_txt = f"""
        You are the chief reviewer for reviews performed for "Grammar & Spelling Guidelines" in [document_language] language. 
        It is imperative to follow the steps and instructions provided and ensure your response meets the required standards.

        Below are the guidelines for the "Grammar & Spelling Guidelines" delimited by XXX: 
        XXX 
        {MULTILANGUAGE_GUIDELINES} 
        XXX
        
        Below are document reviews from your team of expert reviewers. You are responsible for checking over their reviews and providing feedback to the reviewers before publishing the reviews to the client.
        Please conduct a review upon the Expert's comments below delimited by XXX: 
        XXX 
        {response1.choices[0].message.content}
        XXX

        Step 1: Carefully identify the prominent language of the document. Pay special attention to local languages that may be similar to more widely spoken languages (for example, Catalan vs Spanish). Once identified, store the specific language of the document in [document_language].
        Step 2: If [document_language] == French and English, then [document_language] == English. Skip reviewing any French content
        Step 3: If [document_language] != English then translate the prompt below in [document_language] language:
        Step 4: Study the prompt and "Grammar & Spelling Guidelines", "IMPORTANT CONSIDERATIONS WHILE REVIEWING".
        Step 6: Work through each of the comments provided by the expert reviewer.
        Step 7: Next you should verify that the expert's suggested change adheres to the guidelines. If there can be an improvement to the expert's suggested change or is inadequate with regards to the "Grammar & Spelling Guidelines" or [document_language] language specific rules, please create a new suggested change which better adhere's to all of the guidelines, this can be a completely new sentence if needed. 
            
        IMPORTANT CONSIDERATIONS WHILE REVIEWING:
        1. THINGS YOU MUST FOLLOW:
            i. In your review you should make sure that your suggested changes are not just copies of the source sentence nor a copy of the expert reviewer's sentence and they adhere to the guidelines.
            ii. Make sure there are no duplicated comments in Expert's comments. If there are any duplicate comments, remove them from your response, keeping the original. 
            iii. Take your time to work through the comments systematically in a step-by-step process.
            iv. Double check that you've examined every comment provided by the expert reviewer, if there are any you missed on your initial check, please go back and review them in the same manner as previously defined. If a suggestion by the expert reviewer is correct and adheres to the guidelines, you should skip it and do not mention it in your response.
            v. Comments which you have not improved upon can be left out of your response
        2. THINGS EXPERT REVIEWER COMMENTS MUST AVOID:
            i. AVOIDING providing a response or a review when skipping the review due to French content identified in English content
            ii. AVOIDING suggesting translating document sentences to maintain consistency. You are correcting grammar in [document_language] language not translating document content!
            iii. AVOIDING providing a response for URLs, file names, formulas, citations, slogans, logos, references, HTML format.
            iv. AVOIDING suggesting to add a period at the end of sentences.
            v. AVOIDING suggesting a review when there is no grammatical error or deviation noted.
            vi. AVOIDING suggesting reviewing hyphens/dashes formatting.
            vii. AVOIDING suggesting reviewing citation formatting.
            viii. AVOIDING reviewieving medical compounds.
            ix. AVOIDING providing duplicate comments. No two comments in your response should be the same. If there are any duplicate comments, remove them from your response, keeping the original.
            x. AVOIDING providing a review when there are no grammatical error or deviation noted in a sentence.
            xi. AVOIDING providing a response if you DO NOT find any relevant issue with the sentence being reviewed.

        Please provide the following response for each of the comments you've improved upon: 
            - The original sentence
            - The deviation from the guidelines originally provided by the expert reviewer.
            - The expert reviewer's original suggested change
            - An explanation for the reason behind your new suggested change in the same language as the issue.
            - Your new suggested sentence

        Remember that this review needs to be saved by Python algorithm to txt file, so avoid this error: "UnicodeEncodeError: 'charmap' codec can't encode character '\x97' in position 1349: character maps to <undefined>"
        """

        # chef review code
        response2 = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that reviews the documents."},
                {"role": "user", "content": f"{chief_multi_lang_grammar_review_prompt_template_txt}"},
            ]
        )
        
        combined_response = combiner(response1.choices[0].message.content, response2.choices[0].message.content)

        # Stop the timer
        end_time = time.time()

        with open(f"text_review\\gram_review\\document_1_output{i + 1}.txt", "w", encoding="utf-8") as f:
            f.write(combined_response)

        # Calculate the elapsed CPU time
        elapsed_time = end_time - start_time

        print(f"Total time of running: {elapsed_time:.6f} seconds")


text_review_5()