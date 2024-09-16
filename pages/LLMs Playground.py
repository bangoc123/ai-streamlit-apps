import streamlit as st
import requests
import uuid
st.set_page_config(layout="wide") 

# Set up the Streamlit interface
page = st.title("Assignment 3 - Build LLMs Playground")
page = st.markdown("""
    Assignment 3 - ProtonX AI for devs
""")

st.session_state.flask_api_url = "https://7274-34-74-112-255.ngrok-free.app/chat"  # Set your Flask API URL here

col1, col3, col2 = st.columns([6, 0.1, 3])

# Generate a random session ID
session_id = str(uuid.uuid4())

# Initialize chat history in session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Display the chat history using chat UI
with col1:
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Accept user input
    if prompt := st.chat_input("What is up?"):
        # Add user message to chat history
        st.session_state.chat_history.append({"role": "user", "content": prompt})

        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)

        # Prepare the payload for the request
        payload = {
            "message": {"content": prompt},
            "context": st.session_state.chat_history,
            "sessionId": session_id,
            "model": st.session_state.selected_model,
            "temperature": st.session_state.temperature,
            "top_p": st.session_state.top_p,
            "stream": True  # Enable streaming
        }

        # Stream the response from the Flask API
        with st.chat_message("assistant"):
            streamed_content = ""  # Initialize an empty string to concatenate chunks
            response = requests.post(st.session_state.flask_api_url, json=payload, stream=True)

            # Create a placeholder to update the markdown
            response_placeholder = st.empty()

            # Check if the request was successful
            if response.status_code == 200:
                for chunk in response.iter_content(chunk_size=None, decode_unicode=True):
                    if chunk:
                        streamed_content += chunk  # Concatenate each chunk
                        # Update the placeholder with the concatenated content in real-time
                        response_placeholder.markdown(streamed_content)

                # Once complete, add the full response to the chat history
                st.session_state.chat_history.append({"role": "assistant", "content": streamed_content})
            else:
                st.error(f"Error: {response.status_code}")

# Sidebar settings for model, temperature, and top_p
with col2:
    st.session_state.selected_model = st.selectbox(
        "Model", ("gpt-4o", "gpt-4")
    )
    st.write("You selected:", st.session_state.selected_model)

    st.session_state.temperature = st.slider("Temperature", 0.0, 1.0, 0.1)
    st.write("Current Temperature:", st.session_state.temperature)

    st.session_state.top_p = st.slider("Top p", 0.0, 1.0, 1.0)
    st.write("Current Top p:", st.session_state.top_p)
