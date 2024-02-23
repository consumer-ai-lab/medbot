FROM python:3.10.13-bookworm

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

# install postgresql client
RUN apt-get update && apt-get install -y postgresql-client && rm -rf /var/lib/apt/lists/*

# Copy wait-for-postgres.sh and make it executable
COPY question_answer/wait-for-postgress.sh /wait-for-postgres.sh
RUN chmod +x ./wait-for-postgres.sh

EXPOSE 80

CMD ["./wait-for-postgres.sh", "postgres", "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "80"]