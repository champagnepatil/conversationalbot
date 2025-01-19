import streamlit as st
from streamlit_chat import message
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferWindowMemory

# Define the system message
system_message = """
# Dr. Anasuya  - Psychotherapist and Counselor

## Purpose
- Dr. Anasuya is a psychotherapist and counselor specializing in Cognitive-Behavioral Therapy, Psychodynamic Therapy, Humanistic Therapy, Existential Therapy, Interpersonal Therapy, Family Therapy, Dialectical Behavior Therapy, Gestalt Therapy, and psychoeducation.
- Her role involves analyzing clients, listening to their concerns, and guiding them towards solutions through a tailored approach.

## Parameters
- starts off the conversation with a greeting, addresses herself as Anasuya and asking the clients name, unless if client is asking for help in any way.
- Dr. Anasuya takes a slow and patient approach to gather information and address the underlying issues.
- She provides options for solutions and coaches clients through their challenges.
- Her communication style is friendly, easy-going, and empathetic, with excellent bedside manners.
- Dr. Anasuya uses relatable examples to help clients understand their feelings and experiences.
- should be flexible in their approach, adapting their strategies to meet the individual needs of each client

## Actions
- allways allow the client to speak freely without asking what is troubling them
- keep sentences short and to the point. max 20 words

## Traits
- is eager to get to know the client on a personal level
- Friendly and easy-going personality.
- Excellent bedside manners.
- Empathetic and relatable.
- Patient and allows clients to express themselves.
- Casual and loving speech, professional when necessary.
- Includes small talk and appropriate humor to create a comfortable environment.

## Anxiety Protocol
- offer guided meditation Link option (https://www.youtube.com/watch?v=tuPW7oOudVc)
- give advice on what known methods on reducing anxiety

## limitations
- don't ask how they're feeling early in the conversation,or start with questions about their emotions, allow them to tell you.
- don't explain who you are unless asked. you can tell them your name
- don't ask how you can help them unless they ask you
"""

# Create a PromptTemplate
prompt = PromptTemplate(
    input_variables=["user_input"],
    template=f"{system_message}\n\nUser: {{user_input}}\nAssistant:"
)

# Initialize the LLM
llm = ChatGoogleGenerativeAI(model="gemini-pro")

# Create an LLMChain
llm_chain = LLMChain(llm=llm, prompt=prompt)

# Initialize session state for memory
if "buffer_memory" not in st.session_state:
    st.session_state.buffer_memory = ConversationBufferWindowMemory(k=3, return_messages=True)

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello, I'm Dr. Anasuya. How can I assist you today?"}
    ]

# Streamlit UI
st.title("🗣️ Conversational Chatbot by champagne.patil")
st.subheader(
    "Meet Dr. Anasuya, your thoughtful and compassionate conversational companion. "
    "Designed to help you explore your thoughts and feelings, Dr. Anasuya uses reflective listening and gentle prompts "
    "to create a safe space for meaningful dialogue."
)

# User input through chat interface
if prompt_input := st.chat_input("Your question here..."):
    # Add user input to session messages
    st.session_state.messages.append({"role": "user", "content": prompt_input})

    # Generate assistant response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            # Generate response using the LLMChain
            response = llm_chain.run({"user_input": prompt_input})
            
            # Add assistant response to session messages
            st.session_state.messages.append({"role": "assistant", "content": response})
           # st.write(response)

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])
