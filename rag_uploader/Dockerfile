FROM python:3.10.13

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

# install postgresql client
RUN apt-get update && apt-get install -y postgresql-client && rm -rf /var/lib/apt/lists/*

EXPOSE 80

CMD ["uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "80","--reload"]