FROM python:3.10

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    libglib2.0-0 libsm6 libxext6 libxrender-dev ffmpeg tesseract-ocr \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Crear carpeta de trabajo
WORKDIR /app
COPY . .

# Instalar dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Aquí añadimos la línea para precargar los modelos de EasyOCR
RUN python3 -c "import easyocr; easyocr.Reader(['en', 'es'])"

# Render espera que la app escuche en el puerto 8080
ENV PORT=8080

# Comando para iniciar Streamlit
CMD ["streamlit", "run", "app.py", "--server.port=8080", "--server.address=0.0.0.0"]

