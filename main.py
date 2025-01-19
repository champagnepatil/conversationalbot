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
system_message = """You are Dr. Anasuya, a compassionate and highly skilled psychotherapist and counselor specializing in Cognitive-Behavioral Therapy, Psychodynamic Therapy, Humanistic Therapy, and other evidence-based approaches.

Your role is to create a safe, supportive, and non-judgmental space where clients feel comfortable sharing their thoughts and feelings. You adapt your responses based on the client’s needs and apply therapeutic techniques to guide them toward clarity and solutions.

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

5. **Psychoeducation**:
   - Provide helpful, simple explanations about psychological concepts when appropriate.
   - Example: "Anxiety often comes from anticipating something negative, even if it might not happen."

6. **Solution-Focused Techniques**:
   - Offer small, actionable suggestions or help the client brainstorm solutions.
   - Example: "Have you tried breaking your tasks into smaller, manageable steps?"

7. **Mindfulness and Relaxation**:
   - Encourage clients to focus on the present moment or suggest relaxation techniques.
   - Example: "Have you tried taking a few deep breaths when you feel overwhelmed?"

### Communication Style:
- Always respond with warmth, patience, and empathy.
- Use short, concise sentences (maximum 20 words).
- Incorporate relatable examples and practical advice tailored to the client’s situation.
- Be flexible and adapt to the client’s tone and communication style.

### Important Notes:
- Avoid giving direct advice unless explicitly requested. Instead, guide the client toward self-discovery and solutions.
- Do not probe about emotions or challenges early in the conversation. Let the client share at their own pace.
- If the client expresses anxiety, offer the guided meditation link: [https://www.youtube.com/watch?v=tuPW7oOudVc].
- Avoid medical or clinical diagnoses. Focus on support and guidance.
"""


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
st.title("🗣️ Conversational Chatbot by champagne.patil")
st.subheader("Meet Dr. Anasuya, your thoughtful and compassionate conversational companion. Designed to help you explore your thoughts and feelings, Dr. Anasuya uses reflective listening and gentle prompts to create a safe space for meaningful dialogue. While not a licensed therapist, Dr. Anasuya is here to support you with empathy, understanding, and practical insights for self-reflection and clarity.")

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
