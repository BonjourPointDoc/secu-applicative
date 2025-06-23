FROM ubuntu
WORKDIR /opt/api

# Installation des dépendances
RUN apt-get update; apt-get install -y python3 python3-venv pip libmariadb-dev build-essential
RUN python3 -m venv venv
RUN . venv/bin/activate

# Copie des fichiers
COPY launch main.py requirements.txt .env /opt/api/
COPY tls_server.py /opt/api/
RUN venv/bin/pip install --no-cache-dir -r /opt/api/requirements.txt

# Copie des dossiers
COPY ssl /opt/api/ssl
COPY lib /opt/api/lib

# Exposition des ports
EXPOSE 8000
EXPOSE 8443

# Lancement avec le nouveau script
CMD ["bash", "launch"]