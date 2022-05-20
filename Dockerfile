FROM python:3.10-slim-buster

WORKDIR /usr/src/app

RUN apt-get update && apt-get install -y \
    build-essential  \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

ENTRYPOINT ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0"]
