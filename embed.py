import os, chromadb
from ollama import Client
from dotenv import load_dotenv

load_dotenv()

documents = [
  "Llamas are members of the camelid family meaning they're pretty closely related to vicuñas and camels",
  "Llamas were first domesticated and used as pack animals 4,000 to 5,000 years ago in the Peruvian highlands",
  "Llamas can grow as much as 6 feet tall though the average llama between 5 feet 6 inches and 5 feet 9 inches tall",
  "Llamas weigh between 280 and 450 pounds and can carry 25 to 30 percent of their body weight",
  "Llamas are vegetarians and have very efficient digestive systems",
  "Llamas live to be about 20 years old, though some only live for 15 years and others live to be 30 years old",
]

ollama = Client(host=os.getenv('HOST'))

client = chromadb.Client()
collection = client.create_collection(name="docs")

# store each document in a vector embedding database
for i, d in enumerate(documents):
  response = ollama.embeddings(model="mxbai-embed-large", prompt=d)
  embedding = response["embedding"]
  collection.add(
    ids=[str(i)],
    embeddings=[embedding],
    documents=[d]
  )

# prompt
prompt = "How tall llama can grow?"

# generate an embedding for the prompt and retrieve the most relevant doc
response = ollama.embeddings(
  model="mxbai-embed-large",
  prompt=prompt
)

print(response)

results = collection.query(
  query_embeddings=[response["embedding"]],
  n_results=3
)
data = results['documents'][0]

print(data)

# generate a response combining the prompt and data we retrieved in step 2
output = ollama.generate(
  model="llama3",
  prompt=f"Using this data: {data}. Respond to this prompt: {prompt}"
)

print(output['response'])