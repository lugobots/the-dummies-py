FROM python:3.9-slim-buster

WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

COPY main.py /app/main.py
COPY my_bot.py /app/my_bot.py

CMD ["python", "main.py"]

