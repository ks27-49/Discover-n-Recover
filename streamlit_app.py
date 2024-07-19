import streamlit as st
from groq import Groq

# Set up the Streamlit page
st.set_page_config(page_icon="👩‍⚕️", layout="wide", page_title="Discover&Recover")

# Define a function to display the AI response in a non-editable chat box
def display_ai_response(response):
    st.subheader("Rehabilitation Plan")
    st.markdown(response, unsafe_allow_html=True)  # Use markdown for better formatting

# Initialize session state to store the AI-generated response
if "ai_response" not in st.session_state:
    st.session_state.ai_response = ""  # Store AI response

# Function to call the AI API for exercise recommendations
def get_ai_exercises(symptoms):
    # Initialize Groq client
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
    
    # Context message for the AI
    context_message = (
        "You are a physical therapist creating a detailed 3-week rehabilitation plan for an athlete. "
        "Provide specific exercises for each week, including detailed instructions for each exercise. "
        "For each exercise, include the number of sets, repetitions, and duration or time. Format the output as follows: "
        "\nWeek 1:"
        "\n- **Exercise 1:** [Description] - [Sets] sets of [Reps] reps, [Time] seconds each"
        "\n- **Exercise 2:** [Description] - [Sets] sets of [Reps] reps, [Time] seconds each"
        "\n- **Exercise 3:** [Description] - [Sets] sets of [Reps] reps, [Time] seconds each"
        "\n- **Exercise 4:** [Description] - [Sets] sets of [Reps] reps, [Time] seconds each"
        "\n- **Exercise 5:** [Description] - [Sets] sets of [Reps] reps, [Time] seconds each"
        "\nWeek 2:"
        "\n- **Exercise 1:** [Description] - [Sets] sets of [Reps] reps, [Time] seconds each"
        "\n- **Exercise 2:** [Description] - [Sets] sets of [Reps] reps, [Time] seconds each"
        "\n- **Exercise 3:** [Description] - [Sets] sets of [Reps] reps, [Time] seconds each"
        "\n- **Exercise 4:** [Description] - [Sets] sets of [Reps] reps, [Time] seconds each"
        "\n- **Exercise 5:** [Description] - [Sets] sets of [Reps] reps, [Time] seconds each"
        "\nWeek 3:"
        "\n- **Exercise 1:** [Description] - [Sets] sets of [Reps] reps, [Time] seconds each"
        "\n- **Exercise 2:** [Description] - [Sets] sets of [Reps] reps, [Time] seconds each"
        "\n- **Exercise 3:** [Description] - [Sets] sets of [Reps] reps, [Time] seconds each"
        "\n- **Exercise 4:** [Description] - [Sets] sets of [Reps] reps, [Time] seconds each"
        "\n- **Exercise 5:** [Description] - [Sets] sets of [Reps] reps, [Time] seconds each"
        "\nMake sure the response includes exactly three weeks of exercises and is structured accordingly."
    )
    
    # Prepare the messages for completion
    messages_for_completion = [
        {"role": "system", "content": context_message},
        {"role": "user", "content": symptoms}
    ]
    
    # Call the AI API to get exercise recommendations
    completion = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=messages_for_completion,
        temperature=1,
        max_tokens=4096,  # Increased token limit for detailed responses
        top_p=1,
        stream=True
    )
    
    # Process the completion response
    response_chunks = []
    for chunk in completion:
        if chunk.choices:
            chunk_content = chunk.choices[0].delta.content
            if chunk_content:
                response_chunks.append(chunk_content)
    
    # Combine all response chunks into a single string
    full_response = "".join(response_chunks).strip()
    
    return full_response

# Collect user input and generate exercises
with st.form(key="user_input_form"):
    prompt = st.text_area("What symptoms are you experiencing?", key="user_input")
    submit_button = st.form_submit_button("Send")

    if submit_button and prompt:
        # Call the AI API to get exercise recommendations
        ai_generated_response = get_ai_exercises(prompt)
        
        # Update session state with AI-generated response
        st.session_state.ai_response = ai_generated_response
        
        # Clear previous display and show the new response
        st.experimental_rerun()
    elif submit_button:
        st.warning("Please enter your symptoms to continue.")

# Display the AI response if available
if st.session_state.ai_response:
    display_ai_response(st.session_state.ai_response)
