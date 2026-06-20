import gradio as gr
import requests
import os
from dotenv import load_dotenv

load_dotenv(override=True)
port = os.getenv("BACKEND_PORT", "8000")
backend_container = os.getenv("BACKEND_CONTAINER", "localhost")


def chat(message, history):
    messages = message
    BaseURL = f"http://{backend_container}:{port}" # use this in production
    #BaseURL = f"http://localhost:8000" # to be used in local development
    endpoint = "/interactive-agent/interactive-agent"
    url = BaseURL + endpoint
    params = {
        "message": messages
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        return data.get('result', 'No result found')
    except requests.exceptions.RequestException as e:
        print(f"Error occurred: {e}")
        return "Error occurred while fetching response"
    

demo = gr.ChatInterface(
    fn=chat
    )
demo.launch(server_name="0.0.0.0", server_port=7861)