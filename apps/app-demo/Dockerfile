FROM python:3.12-slim

WORKDIR /app

# Instala as dependencias primeiro (cache de layer mais eficiente)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o codigo da aplicacao
COPY app.py .

# Documenta a porta que a app usa
EXPOSE 8080

# Roda como usuario nao-root (boa pratica de seguranca)
RUN useradd -m appuser
USER appuser

CMD ["python", "app.py"]