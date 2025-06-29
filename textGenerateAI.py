import requests

HF_TOKEN = "API_KEY_HERE"
API_URL = "https://api-inference.huggingface.co/models/HuggingFaceH4/zephyr-7b-beta"
HEADERS = {"Authorization": f"Bearer {HF_TOKEN}"}

def generate_aita_story():
    prompt = """<|system|>
You are a helpful assistant that writes Reddit AITA posts.
<|user|>
Write a short, dramatic AITA Reddit post from a first-person point of view, including details and ending with 'AITA?' Also add brackets, age and gender letter in this format (29F)
"""

    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 350,
            "temperature": 0.8,
            "do_sample": True,
            "return_full_text": False
        }
    }

    response = requests.post(API_URL, headers=HEADERS, json=payload)

    if response.status_code == 200:
        result = response.json()
        return result[0]["generated_text"].strip()
    else:
        return f"Error {response.status_code}: {response.text}"

if __name__ == "__main__":
    print("\n--- AITA Story ---\n")
    print(generate_aita_story())
