import streamlit as st
import requests
import json

# Define the endpoint URL
API_ENDPOINT = "https://b227-34-74-136-120.ngrok-free.app/chat"

# Streamlit UI setup
st.title("LLAMA 3.2 Multimodal")
st.write("Enter the image URL and prompt to extract text")

# Input fields for image URL and prompt
image_url = st.text_input("Image URL:", placeholder="Enter the image URL here")
prompt = st.text_area("Prompt:", placeholder="Enter a prompt or leave it blank to extract all text from the image")

# Create two columns
col1, col2 = st.columns(2)

# Display the image in the left column if a valid URL is provided
with col1:
    if image_url:
        st.image(image_url, caption="Uploaded Image", use_column_width=True)

# Extract text when the button is clicked
with col2:
    if st.button("Extract Text"):
        if not image_url:
            st.error("Please provide an image URL.")
        else:
            # Prepare the API request payload
            payload = {
                "image_url": image_url,
                "prompt": prompt
            }
            
            try:
                # Make the POST request to the Flask API
                response = requests.post(API_ENDPOINT, json=payload)
                
                if response.status_code == 200:
                    data = response.json()
                    st.markdown("### Extracted Content")
                    st.markdown(data["content"])
                else:
                    st.error("Error: " + response.json().get("error", "Unable to extract text"))
            except requests.exceptions.RequestException as e:
                st.error(f"Error connecting to the API: {e}")
