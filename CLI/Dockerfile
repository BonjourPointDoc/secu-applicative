FROM ubuntu

WORKDIR /opt/cli

# Installer les dépendances système, y compris pour construire des paquets Python compilés
RUN apt-get update && \
    apt-get install -y python3 python3-venv python3-pip \
        libmariadb-dev build-essential curl \
        libssl-dev libffi-dev && \
    rm -rf /var/lib/apt/lists/*

# Créer l'environnement virtuel Python
RUN python3 -m venv venv

# Activer le venv et installer les dépendances Python
RUN /opt/cli/venv/bin/pip install --upgrade pip && \
    /opt/cli/venv/bin/pip install cryptography

# Copier ton script
COPY tls_server.py /opt/cli/

# Générer les certificats auto-signés
RUN mkdir -p /opt/cli/ssl && \
    openssl req -x509 -nodes -days 365 \
        -newkey rsa:2048 \
        -keyout /opt/cli/ssl/key.pem \
        -out /opt/cli/ssl/cert.pem \
        -subj "/CN=localhost"

# Exposer le port
EXPOSE 8443

# Démarrage du serveur TLS
CMD ["/opt/cli/venv/bin/python", "/opt/cli/tls_server.py"]
