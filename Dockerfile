FROM  python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

COPY .env .

WORKDIR /app/src

EXPOSE 8000

CMD "uvicorn" "main:app" "--reload"

