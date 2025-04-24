import streamlit as st
from openai import OpenAI
import time

# Set up the app
st.set_page_config(page_title="Insurance Chatbot", page_icon="🤖")
st.title("🤖 Insurance Policy Assistant")
st.caption("Ask me about health, auto, or home insurance policies!")

# Initialize OpenAI client - PASTE YOUR API KEY HERE
client = OpenAI(api_key="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")

# Sample insurance knowledge base
INSURANCE_KNOWLEDGE = """
## Health Insurance
- Annual deductible: $1,500 individual / $3,000 family
- Office visits: $30 copay for primary care, $50 for specialists
- Emergency room: $300 copay
- Prescriptions: $10/$40/$80 (generic/brand/specialty)

## Auto Insurance
- Liability coverage: $50,000 per person / $100,000 per accident
- Collision deductible: $500
- Comprehensive deductible: $250
- Roadside assistance: Included

## Home Insurance
- Dwelling coverage: Up to $500,000
- Personal property: 50% of dwelling coverage
- Deductible: 1% of dwelling coverage
- Additional living expenses: Up to 12 months

## Claims Process
1. Report claim online or by phone
2. Adjuster assigned within 24 hours
3. Documentation submission
4. Claim decision within 5 business days
"""

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! I can answer questions about your insurance policies. What would you like to know?"}
    ]

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Function to get chatbot response
def get_ai_response(user_query):
    system_prompt = f"""
    You are a knowledgeable insurance assistant. Use this information to answer questions:
    {INSURANCE_KNOWLEDGE}
    
    Rules:
    - Be polite and professional
    - If you don't know the answer, say "I'm not sure about that, let me connect you with a human agent"
    - Keep answers concise but helpful
    - For premium questions, explain factors that affect pricing
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                *[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
                {"role": "user", "content": user_query}
            ],
            temperature=0.3
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Sorry, I'm having trouble responding. Error: {str(e)}"

# Chat input
if prompt := st.chat_input("Ask your insurance question..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Display assistant response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        # Simulate streaming response
        ai_response = get_ai_response(prompt)
        for chunk in ai_response.split():
            full_response += chunk + " "
            time.sleep(0.05)
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": full_response})

# Sidebar with instructions
with st.sidebar:
    st.markdown("## How to Use")
    st.markdown("""
    1. Type your insurance question
    2. Get instant answers about:
       - Policy coverage
       - Claims process
       - Premiums
       - Deductibles
    3. Complex questions will be escalated
    """)
    
    st.markdown("## Sample Questions")
    st.markdown("""
    - What's my health insurance deductible?
    - Does auto insurance cover rental cars?
    - How do I file a home insurance claim?
    - What affects my premium rates?
    """)
    
    st.markdown("---")
    st.caption("Note: This is a demo chatbot. For actual policy details, please consult your documents.")
