import vertexai 
from vertexai.generative_models import GenerativeModel

PROJECT_ID = 'gemini-explorer-435119'
vertexai.init(project=PROJECT_ID, location='us-central1')

model = GenerativeModel('gemini-1.5-flash-002')
response = model.generate_content("What should I call my new puppy?")

print(response.text)