import streamlit as st
import requests
import base64
import uuid
from audio_recorder_streamlit import audio_recorder

st.title("Speech-to-Text with Ngrok")

# Generate a random session ID
session_id = str(uuid.uuid4())

# Initialize the session state for the backend URL and chat history
if "asr_flask_api_url" not in st.session_state:
    st.session_state.asr_flask_api_url = None

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Function to set the URL
def setup_backend():
    st.markdown(
        """
        ### Setup Backend
        Run the backend [here](https://colab.research.google.com/drive/125JxHsVRrKUQUMOA3h9knlUiuM7OBYlk?usp=sharing) and paste the Ngrok link below.
        """
    )
    link = st.text_input("Backend URL", "")
    if st.button("Save"):
        st.session_state.asr_flask_api_url = f"{link}/speech-to-text"  # Update ngrok URL
        st.rerun()  # Re-run the app to apply changes

# Display the setup only if the URL is not set
if st.session_state.asr_flask_api_url is None:
    setup_backend()

# Once the URL is set, display it or proceed with other functionality
if st.session_state.asr_flask_api_url:
    st.write(f"Backend is set to: {st.session_state.asr_flask_api_url}")

# Record audio using the audio_recorder component
audio_bytes = audio_recorder()

# If audio is recorded, display it and send it to the backend
if audio_bytes:
    st.audio(audio_bytes, format="audio/wav")
    
    # Convert the audio bytes to a base64 encoded string
    audio_base64 = base64.b64encode(audio_bytes).decode('utf-8')

    # Convert the base64 string back to a byte array
    audio_array = list(base64.b64decode(audio_base64))

    # Prepare the payload for the request
    payload = {
        "buffer": {"data": audio_array},
    }
    
    # Send the POST request to the Flask API
    response = requests.post(st.session_state.asr_flask_api_url, json=payload)

    # Check if the request was successful
    if response.status_code == 200:
        # Get the response from the API
        api_response = response.json()
        
        # Display the transcription
        st.write("Transcription: ", api_response['text'])
        
        # Add the assistant's response to the chat history
        st.session_state.chat_history.append({"role": "assistant", "content": f"Transcription: {api_response['text']}"})
    else:
        st.error(f"Error: {response.status_code}")

# Display the chat history using chat UI
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
