# Gemini-API

This repository provides a Python-based API for interacting with Google's Gemini model. It includes different file inputs and chat history support, allowing users to continue conversations across different sessions.

## Installation

### Step 1: Clone the Repository

First, clone this repository to your local machine:
```
git clone https://github.com/Reighto/Gemini-API.git
cd Gemini-API
```
### Step 2: Set Up a Virtual Environment

It is recommended to use a virtual environment to manage dependencies. Here's how you can set it up:

On Windows:
```
python -m venv pyenv
pyenv\Scripts\activate
```
On Linux/MacOS:
```
python3 -m venv pyenv
source pyenv/bin/activate
```
### Step 3: Install Dependencies

Install the necessary Python packages using the requirements.txt file:
```
pip install -r requirements.txt
```
### Step 4: Set Up Your API Key

To use the Gemini API, you'll need an API key from [Google AI Studio](https://aistudio.google.com/app/apikey).

Option 1: Set Up API Key via Environment Variable
```
export API_KEY="your_api_key_here"  # For Unix/Linux/MacOS
set API_KEY="your_api_key_here"     # For Windows
```
Option 2: Hardcode Your API Key **(not recommended for production)**

In the gemini.py file, uncomment the following line and replace your_api_key_here with your actual API key:
```
genai.configure(api_key="your_api_key_here")
```

### Chat History

The API supports chat history. Chat sessions are saved in JSON files named according to the chat name you provide. These files are stored in the directory from which you run the script.

### Example Usage

An example usage script is provided in example.py. This script demonstrates how to interact with the Gemini API using the provided core functions in gemini.py.

To run the example script:
```
python example.py
```
### Custom Usage

To use the API in your own scripts, import the necessary functions from gemini.py and customize them according to your needs.

## License

This project is licensed under the MIT License.
