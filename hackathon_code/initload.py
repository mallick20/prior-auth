import os
import PyPDF2
import requests

# Function to extract text from a PDF file
def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text() + "\n"
    return text

# Function to call OpenAI API
def call_openai_api(prompt, api_key):
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "gpt-3.5-turbo",  
        "messages": [{"role": "user", "content": prompt}]
    }
    


    print(headers)



    print()
    print()


    print(data)



    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return None

# Function to chunk text for API requests
def chunk_text(text, max_tokens=3000):
    words = text.split()
    chunks = []
    current_chunk = []

    for word in words:
        current_chunk.append(word)
        if len(current_chunk) >= max_tokens:
            chunks.append(" ".join(current_chunk))
            current_chunk = []
    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks

# Main function to process PDFs in a folder
def process_pdfs_in_folder(folder_path, api_key):
    for filename in os.listdir(folder_path):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(folder_path, filename)
            print(f"Processing: {pdf_path}")
            pdf_text = extract_text_from_pdf(pdf_path)
            
            # Chunk the extracted text
            chunks = chunk_text(pdf_text)
            for chunk in chunks:
                response = call_openai_api(chunk, api_key)
                print(f"Response from API for {filename}: {response}\n")


# Set your API key and folder path
API_KEY = "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"
FOLDER_PATH = "policydocs"

# Run the processing function
process_pdfs_in_folder(FOLDER_PATH, API_KEY)
