# Usando uma imagem base Python
FROM python:3.10-slim

# Definir o diretório de trabalho no container
WORKDIR /app

# Copiar os arquivos do seu projeto para o diretório de trabalho no container
COPY . /app

# Instalar as dependências do seu projeto
RUN pip install --no-cache-dir -r requirements.txt

# Expor a porta que o Dash vai rodar
EXPOSE 8080

# Comando para rodar o aplicativo Dash com Gunicorn
CMD ["gunicorn", "app:server", "--bind", "0.0.0.0:8080"]
