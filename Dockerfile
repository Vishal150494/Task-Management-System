FROM python:3.10-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

ENV FLASK_APP=src/main.py
ENV FLASK_ENV=dev

CMD [ "flask", "run" "--host=0.0.0.0" ]
