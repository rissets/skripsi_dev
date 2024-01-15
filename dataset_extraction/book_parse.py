import PyPDF2
from transformers import AutoTokenizer
import json
import requests
import re

HOST = 'https://arabia-sas-brooks-charts.trycloudflare.com '
URI = f'https://{HOST}/v1/chat/completions'
tokenizer = AutoTokenizer.from_pretrained("TheBloke/Magicoder-S-DS-6.7B-GPTQ")
history = {'internal': [], 'visible': []}
command = "You are an API that converts bodies of text into a single question and answer into a JSON format. Each JSON " \
          "contains a single question with a single answer. Only respond with the JSON and no additional text. \n"

def run(user_input, history):
    request = {
        "messages": [
            {"content": user_input, "role": "system", "history": history, "message_id": "0"}
        ],
        "mode": "instruct",
        "instruction_template": "Vicuna-v1.1",
        "character": "Example",
        "temperature": 0.7,
        "top_p": 0.1,
        "typical_p": 1,
        "epsilon_cutoff": 0,
        "eta_cutoff": 0,
        "tfs": 1,
        "top_a": 0,
        "repetition_penalty": 1.18,
        "top_k": 40,
        "min_length": 0,
        "no_repeat_ngram_size": 0,
        "num_beams": 1,
        "penalty_alpha": 0,
        "length_penalty": 1,
        "early_stopping": False,
        "mirostat_mode": 0,
        "mirostat_tau": 5,
        "mirostat_eta": 0.1,
        "seed": -1,
        "add_bos_token": True,
        "truncation_length": 2048,
        "ban_eos_token": False,
        "skip_special_tokens": True,
        "stopping_strings": [],
    }

    try:
        response = requests.post(URI, json=request)
        print(response.status_code)
        if response.status_code == 200:
            response_json = response.json()
            print(response_json)

            return response_json["choices"][0]["message"]["content"]
        else:
            print(f"Request failed with status code: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None

def extract_text_from_pdf(file_path):
    pdf_file_obj = open(file_path, 'rb')
    pdf_reader = PyPDF2.PdfReader(pdf_file_obj)
    text = ''
    for page_num in range(len(pdf_reader.pages)):
        page_obj = pdf_reader.pages[page_num]
        text += page_obj.extract_text()
    pdf_file_obj.close()
    return text

def tokenize(text):
    enc = tokenizer.encode(text)
    return enc

def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

def is_json(data):
    try:
        json.loads(data)
        return True
    except ValueError:
        return False


def submit_to_api(chunk, retries=3):
    for i in range(retries):
        try:
            response = run(command + chunk.strip(), history)

            if response is not None:
                if is_json(response):
                    print(f"Attempt {i + 1} succeeded.")
                    print(response)
                    return json.loads(response)
                else:
                    match = re.search(r'`(.*?)`', response, re.S)
                    if match and is_json(match.group(1)):
                        print(f"Attempt {i + 1} failed. Retrying...")
                        return json.loads(match.group(1))
                    else:
                        print(response)
                        print(f"Request failed: expected JSON but got {response}")
            else:
                print("Empty response. Retrying...")

        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            continue

    print("Max retries exceeded. Skipping this chunk.")
    return None


text = extract_text_from_pdf('../dataset/golang-generic.pdf')
tokens = tokenize(text)

token_chunks = list(chunks(tokens, 150))

responses = []

for chunk in token_chunks:
    response = submit_to_api(tokenizer.decode(chunk))
    if response is not None:
        responses.append(response)

# Write responses to a JSON file
with open('responses.json', 'w') as f:
    json.dump(responses, f)
