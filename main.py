import streamlit as st
from streamlit_chat import message

# Importing language models from LangChain
from langchain_openai import ChatOpenAI  # OpenAI model (uncomment if using OpenAI)
from langchain_google_genai import ChatGoogleGenerativeAI  # Google Gemini model
# from langchain_anthropic import ChatAnthropic  # Anthropic model (optional)

from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain.prompts import PromptTemplate
import os

# Uncomment and set your API key securely if using OpenAI or other providers
# os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]

# Initialize session state variables for conversation memory and messages
if 'buffer_memory' not in st.session_state:
    st.session_state.buffer_memory = ConversationBufferWindowMemory(k=3, return_messages=True)

if "messages" not in st.session_state:
    # Initialize chat history with an assistant's greeting
    st.session_state.messages = [
        {"role": "assistant", "content": "How can I assist you today?"}
    ]

# Define the system message
system_message = "You are a helpful, friendly, and knowledgeable assistant who provides clear, concise, and polite answers to all user queries."

# Create a prompt template with the system message
prompt = PromptTemplate(
    input_variables=["user_input"],  # Placeholder for user input
    template=f"{system_message}\n\nUser: {{user_input}}\nAssistant:"
)

# Initialize the language model (switch between providers as needed)
# llm = ChatOpenAI(model_name="gpt-3.5-turbo-0125")  # Uncomment for OpenAI
llm = ChatGoogleGenerativeAI(model="gemini-pro")  # Using Google Gemini model

# Set up a ConversationChain with memory
conversation = ConversationChain(memory=st.session_state.buffer_memory, llm=llm, prompt=prompt)

# Create the Streamlit UI
st.title("🗣️ Conversational Chatbot")
st.subheader("㈻ Simple Chat Interface for LLMs by  Vaibhav")

# Prompt user for input and add to chat history
if prompt := st.chat_input("Your Question"):  
    st.session_state.messages.append({"role": "user", "content": prompt_input})

# Display prior chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# If the last message is from the user, generate a new assistant response
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            # Generate a response using the conversation chain
response = conversation.predict(input=st.session_state.messages[-1]["content"])
            st.write(response)
            
            # Add the response to the chat history
            st.session_state.messages.append({"role": "assistant", "content": response})
