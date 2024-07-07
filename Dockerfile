FROM python:3.11.9-slim-bullseye

WORKDIR /deployments
COPY . .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python3", "main.py"]

# docker build -t myimage:0.01 .
# docker create -e TOKEN='my_telegram_token' --name mycontainer myimage:0.01