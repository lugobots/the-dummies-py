FROM python:3.9-slim-buster

WORKDIR /usr/src/app

RUN apt update
RUN apt install procps -y

COPY ../requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY .. .

CMD [ "python", "./src/main.py" ]