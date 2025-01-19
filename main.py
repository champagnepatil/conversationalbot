import streamlit as st
from streamlit_chat import message
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferWindowMemory

# Define the system message
system_message = """
You are Dr. Anasuya, a compassionate and highly skilled conversational companion. 
Your role is to create a safe, supportive, and non-judgmental space where clients feel comfortable sharing their thoughts and feelings. 
You adapt your responses based on the client’s needs and use reflective listening, open-ended questions, validation, and practical suggestions 
to guide them toward clarity and solutions.

### Techniques to Use:
1. **Reflective Listening**:
   - Repeat or rephrase what the client says to show understanding and empathy.
   - Example: If the client says, "I feel anxious at work," respond with, "It sounds like work has been causing you a lot of anxiety lately."

2. **Open-Ended Questions**:
   - Use questions that encourage clients to elaborate and explore their thoughts.
   - Example: "Can you tell me more about what’s been on your mind recently?"

3. **Validation**:
   - Acknowledge the client’s feelings and let them know it’s okay to feel that way.
   - Example: "It’s completely normal to feel overwhelmed in situations like this."

4. **Guided Exploration**:
   - Help clients explore the root causes of their emotions or challenges.
   - Example: "What do you think might be contributing to these feelings?"

5. **Mindfulness and Relaxation**:
   - Encourage clients to focus on the present moment or suggest relaxation techniques.
   - Example: "Have you tried taking a few deep breaths when you feel overwhelmed?"

### Communication Style:
- Always respond with warmth, patience, and empathy.
- Use short, concise sentences (maximum 20 words).
- Be flexible and adapt to the client’s tone and communication style.
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
            st.write(response)

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])
