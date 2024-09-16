import streamlit as st
import requests
from PIL import Image
import io
import re
from streamlit_drawable_canvas import st_canvas

# Flask API URL (replace with the public URL from ngrok)
API_URL = "https://8f86-34-142-165-13.ngrok-free.app/convert_to_latex"

st.title("Chuyên gia giải toán")

# Set up a canvas for drawing
canvas_result = st_canvas(
    fill_color="rgba(255, 165, 0, 0.3)",  # Fill color with some transparency
    stroke_width=2,
    stroke_color="black",
    background_color="white",
    height=300,
    width=600,
    drawing_mode="freedraw",
    key="canvas",
)

def process_and_display(content):
    # Regex pattern to match both inline \( ... \) and block \[ ... \] LaTeX formulas
    pattern = re.compile(r'(\\\[.*?\\\]|\\\(.*?\\\))', re.DOTALL)

    # Split the content based on the pattern
    parts = pattern.split(content)

    # Iterate through parts to check for LaTeX or normal text
    for part in parts:
        if part.startswith("\\[") and part.endswith("\\]"):
            # Block LaTeX formula, display using st.latex
            formula = part[2:-2].strip()  # Remove \[ and \] for st.latex
            st.latex(formula)
        elif part.startswith("\\(") and part.endswith("\\)"):
            # Inline LaTeX formula, display using st.latex
            formula = part[2:-2].strip()  # Remove \( and \) for st.latex
            st.latex(formula)
        else:
            # It's normal text, process and display with st.markdown
            st.markdown(part)

# Check if drawing was made on the canvas
if canvas_result.image_data is not None:
    # Convert the NumPy array (canvas_result.image_data) to a PIL image
    img = Image.fromarray((canvas_result.image_data).astype('uint8'))

    # Add a button to send the image to the API and display the drawn image
    if st.button("Solve it"):
        # Save the image to a buffer (in memory)
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        buf.seek(0)  # Rewind the buffer to the beginning

        # Send the image to the Flask API
        files = {'image': buf}
        response = requests.post(API_URL, files=files)

        # Handle and display the server's response
        if response.status_code == 200:
            result = response.json().get('generated_text', '')
            process_and_display(result)
        else:
            st.error("Failed to get a response from the server")
else:
    st.warning("Please draw something on the canvas to send!")
