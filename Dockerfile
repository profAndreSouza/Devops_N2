# Imagem base oficial do Python 3.11 Slim
FROM python:3.11-slim

# Evita criação de arquivos .pyc e garante logs em tempo real
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Define diretório de trabalho no container
WORKDIR /app

# Instala dependências do sistema necessárias para compilação
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copia o arquivo de dependências e instala os pacotes Python
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copia todo o código-fonte para o container
COPY . /app

# Expõe a porta 5000 para acesso web
EXPOSE 5000

# Comando para iniciar a aplicação Flask escutando em 0.0.0.0
CMD ["python", "app.py"]
