import easyocr
import streamlit as st
from PIL import Image
import numpy as np
import cv2

st.title("OCR Text Extractor")

# Initialize EasyOCR reader
reader = easyocr.Reader(['en'])

# Upload image file
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image', use_container_width=True)
    
    image_np = np.array(image)
    
    # Perform OCR using EasyOCR
    results = reader.readtext(image_np)

    for (bbox, text, prob) in results:
        top_left = tuple(map(int, bbox[0]))
        bottom_right = tuple(map(int, bbox[2]))
        cv2.rectangle(image_np, top_left, bottom_right, (0, 255, 0), 2)

    annotated_image = Image.fromarray(image_np)
    st.image(annotated_image, caption="Detected Text Highlighted", use_container_width=True)

    extracted_text = "\n".join([f"{text} (Confidence: {prob:.2f})" for (_, text, prob) in results])
    st.subheader("Extracted Text:")
    st.text(extracted_text)

    st.download_button(
        label="Download Extracted Text",
        data=extracted_text,
        file_name="extracted_text.txt",
        mime="text/plain",
    )
