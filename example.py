import google.generativeai as genai
import os
import json
import time
import PIL.Image

# Set up your API key
genai.configure(api_key=os.getenv("API_KEY"))

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

# Function to start a new chat session
def start_new_chat():
    global current_chat
    chat_name = input("Enter a name for the new chat: ")
    if chat_name == "":
        print("Invalid name for a chat, continuing previous chat.")
        return load_chat_history(current_chat)
    current_chat = chat_name
    print(f"- - - - Starting a new chat: {chat_name} - - - -")
    return []

# Function to continue a previous chat session
def continue_previous_chat():
    global current_chat
    chat_name = input("Enter the chat name to continue: ")
    current_chat = chat_name
    history = load_chat_history(chat_name)
    if history:
        print(f"- - - - Continuing chat: {chat_name} - - - -")
    else:
        print(f"- - - - No chat history found for '{chat_name}'. Starting a new chat - - - -")
    return history

# Function to check remaining tokens (mocked)
def check_tokens():
    print("Soon")

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
            print("Processing video...")
            time.sleep(5)
            uploaded_file = genai.get_file(uploaded_file.name)
        return uploaded_file
    elif ext in [".mp3", ".wav"]:
        return genai.upload_file(file_path)
    elif ext in [".txt", ".java", ".py"]:
        return process_text_file(file_path)
    else:
        print("Unsupported file type.")
        return None

# Function to process user input and interact with the model
def process_input(user_input, chat_history, prompt_buffer):
    if user_input.lower() == "^stop^" or user_input.lower() == "^exit^":
        save_chat_history(current_chat, chat_history)
        print("- - - - Chat was stopped - - - -")
        return False
    elif user_input.lower() == "^new^":
        chat_history = start_new_chat()
    elif user_input.lower() == "^continue^":
        chat_history = continue_previous_chat()
    elif user_input.lower() == "^tokensleft^":
        check_tokens()
    elif user_input.lower().startswith("^image^") or user_input.lower().startswith("^pdf^") or user_input.lower().startswith("^video^") or user_input.lower().startswith("^audio^") or user_input.lower().startswith("^text^"):
        try:
            _, file_path = user_input.split("^", 1)[1].strip().split(" ", 1)
            file_content = process_file(file_path)
            if file_content:
                prompt_buffer.append(file_content)
            else:
                print(f"Failed to process file: {file_path}")
        except ValueError:
            print("Invalid input format. Use: ^command^ file_path")
    elif user_input == "":  # If input is empty, treat it as a submit command if there's something in the buffer
        if prompt_buffer:
            response = send_combined_message(prompt_buffer, chat_history)
            prompt_buffer.clear()
            print(response)
        else:
            print("No prompt to submit. Add text or files first.")
    else:
        prompt_buffer.append(user_input)

    return True

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

    return "\nGemini: " + response

# Main loop
def run_chat():
    print("- - - - Chat started - - - -")
    chat_history = continue_previous_chat()  # Start by continuing previous chat if it exists
    prompt_buffer = []  # Buffer to hold text and files before submission
    
    while True:
        user_input = input("You: ")
        if not process_input(user_input, chat_history, prompt_buffer):
            break

if __name__ == "__main__":
    run_chat()
