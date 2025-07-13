import os
import easyocr
import streamlit as st
from gtts import gTTS
from googletrans import Translator
import cv2
from PIL import Image
import numpy as np

# Usar carpeta temporal (/tmp en Render)
CARPETA = "/tmp"
os.makedirs(CARPETA, exist_ok=True)

st.title("OCR + Traducción + Voz")

uploaded_file = st.file_uploader("Sube una imagen", type=["jpg", "jpeg", "png"])
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Imagen subida', use_column_width=True)

    image_path = os.path.join(CARPETA, uploaded_file.name)
    image.save(image_path)

    reader = easyocr.Reader(['es', 'en'], gpu=False)
    result = reader.readtext(image_path, detail=0)
    texto_extraido = " ".join(result)
    st.text_area("Texto extraído", value=texto_extraido, height=150)

    if texto_extraido:
        traductor = Translator()
        traduccion = traductor.translate(texto_extraido, dest='en').text
        st.text_area("Traducción al inglés", value=traduccion, height=150)

        tts = gTTS(traduccion, lang='en')
        audio_path = os.path.join(CARPETA, "audio.mp3")
        tts.save(audio_path)

        with open(audio_path, "rb") as audio_file:
            st.audio(audio_file.read(), format="audio/mp3")
