import streamlit as st
import easyocr
import tempfile
import os
from gtts import gTTS
from googletrans import Translator

# Crear carpeta de salida si no existe
os.makedirs("archivos", exist_ok=True)

# --------------------------
# 🎨 Configuración visual
# --------------------------
st.set_page_config(page_title="OCR Web App", page_icon="🧾", layout="wide")

st.markdown(
    "<h1 style='text-align: center; color: #4CAF50;'>🧾 OCR Web App</h1>",
    unsafe_allow_html=True
)
st.markdown("<p style='text-align: center;'>Convierte una imagen en texto, escúchalo o descárgalo fácilmente</p>", unsafe_allow_html=True)

# --------------------------
# 📁 Sidebar: Subir imagen
# --------------------------
with st.sidebar:
    st.header("📤 Subir imagen")
    imagen_subida = st.file_uploader("Selecciona una imagen", type=["png", "jpg", "jpeg"])

    # 🌍 Idioma destino para la traducción
    idioma_destino = st.selectbox("🌐 Traducir a:", ["es", "en", "fr", "de", "it", "pt", "zh-cn"])

    if st.button("🧹 Limpiar todo"):
        st.experimental_rerun()

# --------------------------
# 📸 Procesamiento principal
# --------------------------
if imagen_subida:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp:
        tmp.write(imagen_subida.read())
        ruta_temporal = tmp.name

    lector = easyocr.Reader(['es'])

    with st.spinner("🧐 Extrayendo texto de la imagen..."):
        resultado = lector.readtext(ruta_temporal, detail=0)
        texto = "\n".join(resultado)

    # Traducir texto extraído
    traductor = Translator()
    traduccion = traductor.translate(texto, dest=idioma_destino).text

    # Mostrar imagen y texto en columnas
    col1, col2 = st.columns(2)

    with col1:
        st.image(imagen_subida, caption="🖼 Imagen cargada", use_container_width=True)

    with col2:
        st.subheader("📄 Texto extraído:")
        st.text_area("Resultado OCR:", texto, height=300)

        # Mostrar traducción
        st.subheader("🌍 Traducción:")
        st.text_area(f"Texto traducido ({idioma_destino})", traduccion, height=300)

    # Guardar archivo de texto
    nombre_base = os.path.splitext(imagen_subida.name)[0]
    ruta_txt = f"archivos/{nombre_base}_extraido.txt"
    with open(ruta_txt, "w", encoding="utf-8") as f:
        f.write(texto)

    with open(ruta_txt, "rb") as f:
        st.download_button(
            label="📥 Descargar archivo de texto",
            data=f,
            file_name=os.path.basename(ruta_txt),
            mime="text/plain"
        )

    # ✅ Convertir texto a voz con gTTS
    ruta_mp3 = f"archivos/{nombre_base}.mp3"
    tts = gTTS(text=texto, lang='es')
    tts.save(ruta_mp3)

    # 🔊 Reproductor de audio
    st.subheader("🔊 Escuchar texto:")
    st.audio(ruta_mp3, format="audio/mp3")

    with open(ruta_mp3, "rb") as f:
        st.download_button(
            label="🎧 Descargar audio",
            data=f,
            file_name=os.path.basename(ruta_mp3),
            mime="audio/mp3"
        )

    st.success("✅ Texto extraído y audio generado correctamente.")

    os.remove(ruta_temporal)