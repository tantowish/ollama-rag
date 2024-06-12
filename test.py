import os
from ollama import Client
from dotenv import load_dotenv

load_dotenv()

client = Client(host=os.getenv('HOST'))
response = client.chat(model='llama3', messages=[
  {
    'role': 'user',
    'content': 'Why is the sky blue?',
  },
])
print(response['message']['content'])