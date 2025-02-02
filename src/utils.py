import requests as re
from transformers import PegasusForConditionalGeneration, PegasusTokenizer
import torch
import re as regex

# Ensure your API key is correct
api_key = ''

# Headers for Hugging Face API
headers = {"Authorization": f"Bearer {api_key}"}

# Define utility functions
def truncate_text(text, max_length=500):
    return text[:max_length]

model_name = 'tuner007/pegasus_paraphrase'
torch_device = 'cuda' if torch.cuda.is_available() else 'cpu'
tokenizer = PegasusTokenizer.from_pretrained(model_name)
model = PegasusForConditionalGeneration.from_pretrained(model_name).to(torch_device)


def paraphrase_text(text):
    max_length = 60  # Set your desired max length
    # Prepare the inputs using the tokenizer's __call__ method
    inputs = tokenizer(
        text,
        truncation=True,
        padding='longest',
        max_length=max_length,
        return_tensors="pt").to(torch_device)

    # Generate the paraphrase using the model with sampling
    translated = model.generate(
        **inputs,
        max_length=max_length,
        num_beams=10,
        temperature=1.5,
        do_sample=True
    )

    # Decode the generated text
    tgt_text = tokenizer.batch_decode(translated, skip_special_tokens=True)

    return tgt_text[0]

# Function to check if a paragraph is relevant to a query
def is_relevant(query, paragraph, headers, threshold=0.6):
    API_URL = "https://api-inference.huggingface.co/models/sentence-transformers/all-MiniLM-L6-v2"
    query = truncate_text(query)
    paragraph = truncate_text(paragraph)
    payload = {
        "inputs": {
            "source_sentence": query,
            "sentences": [paragraph]
        }
    }
    response = re.post(API_URL, headers=headers, json=payload)
    response_json = response.json()
    if response_json and isinstance(response_json, list):
      #print(response_json) #Debugging Statement
      similarity = response_json[0]
      return similarity > threshold
    else:
        return False
    
# Function to clean the extracted text
def clean_text(text):
    # Define patterns for headers, footers, and irrelevant sections
    patterns = [
        r"Unit \d+",                          # Unit sections
        r"© Copyright.*",                     # Copyright statements
        r"Figure \d+-\d+.*",                  # Figure labels
        r"Course materials.*",                # Course material notices
        r"1-\d+",                             # Page numbers
        r"Uempty",                            # Placeholder text
        r"IBM Training"                       # Training headers
    ]

    for pattern in patterns:
        text = regex.sub(pattern, '', text)

    return text.strip()




#    similarity = response.json()[0]  # Adjusting to extract the similarity score
#    #print("Similarity:", similarity)  # Debugging statement
#    return similarity > threshold
