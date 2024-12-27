FROM python:3.11-alpine
LABEL authors="mbchl"

WORKDIR /users_service

COPY . .

RUN pip install -r requirements.txt

EXPOSE 8100

CMD ["python", "./main.py"]