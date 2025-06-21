FROM ubuntu

WORKDIR /opt/api

RUN apt-get update; apt-get install -y python3 python3-venv pip libmariadb-dev build-essential
RUN python3 -m venv venv
RUN . venv/bin/activate

COPY launch main.py requirements.txt .env /opt/api/
RUN venv/bin/pip install --no-cache-dir -r /opt/api/requirements.txt

COPY ssl /opt/api/ssl
COPY lib /opt/api/lib

EXPOSE 8000:8000

CMD ["bash", "launch"]