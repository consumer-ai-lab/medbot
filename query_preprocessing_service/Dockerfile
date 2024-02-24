FROM python:3.10.13-bookworm

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt



EXPOSE 80

CMD ["uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "80","--reload"]