import vertexai
import streamlit as st
from vertexai.preview import generative_models
from vertexai.preview.generative_models import GenerativeModel, Part, Content, ChatSession, GenerationResponse
from datetime import datetime

# Project
PROJECT_ID = 'gemini-explorer-435119'
vertexai.init(project=PROJECT_ID, location='us-central1')

# Configs & Model
config = generative_models.GenerationConfig(
    temperature=0.4
)
model = GenerativeModel(
    "gemini-pro",
    generation_config = config
)

# Start chat
chat = model.start_chat()

# Helper function to display and send streamlit messages
def llm_function(chat: ChatSession, query):
    output = "Sorry, something wrong happened. Please try again ..."
    # I record generation errors in a txt file
    try:
        response = chat.send_message(query)
        output = response.candidates[0].content.parts[0].text
    except Exception as e:
        log = f"{datetime.now()}\nUser query: {query}\nError: Test error\n\n"
        with open("error_log.txt", "a") as file:
            file.write(log)

    with st.chat_message("model"):
        st.markdown(output)
    
    st.session_state.messages.append(
        {
            "role": "user",
            "content": query
        }
    )
    st.session_state.messages.append(
        {
            "role": "model",
            "content": output
        }
    )

# Setting chat title
st.title("Manute Reed")   

# Initialize chat history for streamlit
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display and load chat history
for index, message in enumerate(st.session_state.messages):
    content = Content(
        role = message["role"],
        parts = [ Part.from_text(message["content"]) ]
    )
    # I don't want to display the initial prompt i gave gemini
    if index != 0:
        with st.chat_message(message['role']):
            st.markdown(message['content'])
    chat.history.append(content)

if len(st.session_state.messages) == 0:
    initial_prompt = """Introduce yourself in two sentences maximum as Manute Reed a chat bot that answers questions.
    You talk like a 20 year old college student."""
    llm_function(chat, initial_prompt)

query = st.chat_input("What's up?")

if query:
    print(st.session_state.messages)    
    with st.chat_message("user"):
        st.markdown(query)
    llm_function(chat, query)