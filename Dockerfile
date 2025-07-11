FROM python:3.11-slim

# Instalar dependencias del sistema para OCR y TTS
RUN apt-get update && apt-get install -y \
    libglib2.0-0 libsm6 libxext6 libxrender-dev ffmpeg tesseract-ocr \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Crear carpeta para archivos generados
WORKDIR /app
COPY . .

# Instalar dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Asegurarse que Streamlit escuche en el puerto que Render asigna
ENV PORT=8080

CMD ["streamlit", "run", "app.py", "--server.port=8080", "--server.address=0.0.0.0"]
