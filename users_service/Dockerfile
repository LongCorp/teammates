FROM python:3.11-alpine
LABEL authors="mbchl"

WORKDIR /users_service

COPY . .
COPY ./users_service .



RUN pip install -r requirements.txt

EXPOSE 8200

CMD ["python", "./main.py"]