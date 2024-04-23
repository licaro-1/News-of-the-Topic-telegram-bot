FROM python:3.9.5-slim


WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt .

RUN pip install --upgrade pip --no-cache-dir

RUN pip install -r ./requirements.txt --no-cache-dir

COPY ./app ./


CMD ["python", "main.py"]
