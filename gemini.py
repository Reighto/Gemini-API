import google.generativeai as genai
import os
import json
import time
import PIL.Image

# Your API key
genai.configure(api_key=os.getenv("API_KEY"))
# if you prefer hardcoded api key: genai.configure(api_key="your_api_key_here")

# Initialize the model
model = genai.GenerativeModel("gemini-1.5-flash")
chat_history_file_template = "chat_history_{}.json"
current_chat = "default"

# Function to load chat history from a file
def load_chat_history(chat_name):
    file_path = chat_history_file_template.format(chat_name)
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            return json.load(file)
    return []

# Function to save chat history to a file
def save_chat_history(chat_name, history):
    file_path = chat_history_file_template.format(chat_name)
    with open(file_path, 'w') as file:
        json.dump(history, file)

# Function to process text files for the model
def process_text_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

# Function to process files for the model
def process_file(file_path):
    _, ext = os.path.splitext(file_path)
    if ext in [".jpg", ".jpeg", ".png"]:
        return PIL.Image.open(file_path)
    elif ext == ".pdf":
        return genai.upload_file(file_path)
    elif ext in [".mp4", ".avi"]:
        uploaded_file = genai.upload_file(file_path)
        while uploaded_file.state.name == "PROCESSING":
            time.sleep(5)
            uploaded_file = genai.get_file(uploaded_file.name)
        return uploaded_file
    elif ext in [".mp3", ".wav"]:
        return genai.upload_file(file_path)
    elif ext in [".txt", ".java", ".py"]:
        return process_text_file(file_path)
    else:
        return None

# Function to add user input to the prompt buffer
def add_to_prompt_buffer(prompt_buffer, input_data):
    prompt_buffer.append(input_data)

# Function to send a message and get a response with context
def send_combined_message(prompt_buffer, chat_history):
    combined_prompt = []

    # Add the chat history to the combined prompt
    for entry in chat_history:
        if isinstance(entry, str):
            combined_prompt.append(entry)
        elif isinstance(entry, PIL.Image.Image):
            combined_prompt.append("[Image]")
        else:
            combined_prompt.append("[File]")
    
    # Add the current prompt buffer content
    for item in prompt_buffer:
        if isinstance(item, str):
            combined_prompt.append(f"User: {item}")
        elif isinstance(item, PIL.Image.Image):
            combined_prompt.append("[Image]")
        else:
            combined_prompt.append("[File]")

    # Create the final prompt string
    combined_prompt_str = "\n".join(combined_prompt)

    # Generate a response considering the conversation history
    response = model.generate_content(combined_prompt_str).text

    # Append the combined prompt and the model's response to the history
    chat_history.append(f"User: {combined_prompt_str}")
    chat_history.append(f"AI: {response}")

    # Save chat history after each interaction
    save_chat_history(current_chat, chat_history)

    return response

# Example usage:
def run_chat():
    chat_history = load_chat_history("default")  # Continue a default chat
    prompt_buffer = []  # Buffer to hold text and files before submission

    # Example: Adding user text input
    add_to_prompt_buffer(prompt_buffer, "Hello, what do you see in this picture?")
    
    # Example: Adding an image file to the prompt
    image = process_file("/path/to/image.png")
    if image:
        add_to_prompt_buffer(prompt_buffer, image)

    # Submit the prompt buffer and get a response
    response = send_combined_message(prompt_buffer, chat_history)
    print(response)

if __name__ == "__main__":
    run_chat()
