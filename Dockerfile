# Usa uma imagem oficial leve do Python
FROM python:3.11-slim

# Evita que o Python grave ficheiros .pyc no disco e ativa buffer de saída imediato
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Instala dependências do sistema necessárias para Matplotlib e SQLite
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libsqlite3-dev \
    && rm -rf /var/lib/apt/lists/*

# Define o diretório de trabalho no container
WORKDIR /app

# Copia o ficheiro de dependências e instala os pacotes
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo o código-fonte para o container
COPY . .

# Expõe a porta onde o Flet Web vai correr
EXPOSE 8080

# Comando para iniciar a aplicação no modo Web
CMD ["python", "-m", "frontend.app"]