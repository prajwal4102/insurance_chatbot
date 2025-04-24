import streamlit as st
import google.generativeai as genai
import time

GEMINI_API_KEY = "AIzaSyAKUDasjpMc_uui8Ny1PZxhR-JSI6QsG9E" 
genai.configure(api_key=GEMINI_API_KEY)

st.set_page_config(page_title="Insurance Chatbot", page_icon="🤖")
st.title("🤖 Insurance Policy Assistant (Gemini)")
st.caption("Ask me about health, auto, or home insurance policies!")

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

model = genai.GenerativeModel('gemini-1.5-flash-latest')

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! I can answer questions about your insurance policies. What would you like to know?"}
    ]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

def get_ai_response(user_query):
    prompt = f"""
    You are a knowledgeable insurance assistant. Use this information to answer questions:
    {INSURANCE_KNOWLEDGE}
    
    Rules:
    - Be polite and professional
    - If unsure, say "Let me connect you with a human agent"
    - Keep answers concise but helpful
    - Explain factors that affect pricing
    
    Current conversation history:
    {st.session_state.messages}
    
    User question: {user_query}
    """
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"

if prompt := st.chat_input("Ask your insurance question..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        ai_response = get_ai_response(prompt)
        
        for chunk in ai_response.split():
            full_response += chunk + " "
            time.sleep(0.05)
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    
    st.session_state.messages.append({"role": "assistant", "content": full_response})

with st.sidebar:
    st.markdown("## How to Use")
    st.markdown("""
    1. Type your insurance question
    2. Get instant answers about:
       - Policy coverage
       - Claims process
       - Premiums
       - Deductibles
    """)
    
    st.markdown("## Sample Questions")
    st.markdown("""
    - What's my health insurance deductible?
    - Does auto insurance cover rental cars?
    - How do I file a home insurance claim?
    """)
    
    st.markdown("---")
    st.caption("Note: This is a demo chatbot using Gemini AI")
