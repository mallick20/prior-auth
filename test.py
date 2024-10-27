import os
import pandas as pd
import requests

# Function to call OpenAI API
def call_openai_api(prompt, api_key):
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "gpt-3.5-turbo",  # or any other model you want to use
        "messages": [{"role": "user", "content": prompt}]
    }
    
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return None

# Function to convert a row to a formatted string
def format_row_as_string(row):
    return "; ".join([f"{key}: {value}" for key, value in row.items()])

# Function to process CSV and get responses
def process_csv_file(csv_path, api_key, output_file):
    # Read CSV file
    df = pd.read_csv(csv_path)

    with open(output_file, 'w') as f:
        for index, row in df.iterrows():
            # Convert the entire row to a formatted string
            prompt = "I need you to be an Insurance Provider and check my Prior Authorization request.... Give me Yes, Acceptable or No, Rejected and reason for rejecting the claim... Patient Information / Medical History: " + format_row_as_string(row) + "...\n Does " + row['Current Medications Administered'] + " Need any prior authorizations.. And does the existing tests cover those authorization? Please let me know what needs to be done to make sure this drug gets authorized when we apply for Authorization"

            #print(f"Processing: {prompt}")
            response = call_openai_api(prompt, api_key)
            
            if response:
                f.write(f"\nInput: {prompt}\n\nResponse: {response}\n\n---------------------------------------\n")
                #print(f"Response saved for input: {prompt}")


# Set your API key, input CSV file path, and output file path
API_KEY = "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"

CSV_PATH = "final_ehr.csv"
OUTPUT_FILE = "output_file.txt"

# Run the processing function
process_csv_file(CSV_PATH, API_KEY, OUTPUT_FILE)
