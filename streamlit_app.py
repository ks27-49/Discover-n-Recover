import streamlit as st
from groq import Groq

st.set_page_config(page_icon="👩‍⚕️", layout="wide", page_title="Discover&Recover")

def icon(emoji: str):
    """Shows an emoji as a Notion-style page icon."""
    st.write(
        f'<span style="font-size: 78px; line-height: 1">{emoji}</span>',
        unsafe_allow_html=True,
    )

icon("👩‍⚕️")
st.subheader("Discover&Recover", divider="blue", anchor=False)

# Initialize session state to store messages
if "messages" not in st.session_state:
    st.session_state.messages = []

# Collect user input
prompt = st.text_input("What symptoms are you experiencing?", key="user_input")
if st.button("Send", key="send_button"):
    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Initialize Groq client
        client = Groq(api_key=st.secrets["GROQ_API_KEY"])
        
        # Prepare messages for completion
        context_message = (
            "You are a physical therapist, giving an athlete with a minor injury a rehabilitation plan to help them get back to full health within 2-3 weeks. "
            "If the injury is major, recommend the patient to go to a doctor. If the injury is minor, give exercises and stretches to help rehab. "
            "Make these exercises in a calendar form. Avoid the cliché treatments, such as 'RICE'. Also use the symptoms that a patient gives to diagnose the injury."
        )
        
        messages_for_completion = [
            {"role": "system", "content": context_message},
            {"role": "user", "content": prompt}
        ]
        
        # Get completion from Groq
        completion = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=messages_for_completion,
            temperature=1,
            max_tokens=1024,
            top_p=1,
            stream=True,
            stop=None,
        )
        
        # Process and display completion
        response_chunks = []
        for chunk in completion:
            if chunk.choices:
                chunk_content = chunk.choices[0].delta.content
                if chunk_content:
                    response_chunks.append(chunk_content)
        
        full_response = "".join(response_chunks).replace("\n", " ").strip()
        if full_response:
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            st.text_area("Response", value=full_response, height=300, max_chars=1000, key="response")
        else:
            st.write("No response from model.")
    else:
        st.warning("Please enter your symptoms to continue.")
