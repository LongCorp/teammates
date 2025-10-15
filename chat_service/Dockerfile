FROM python:3.11-alpine
LABEL authors="mbchl"

WORKDIR /chat_service

COPY . .

RUN pip install -r requirements.txt

EXPOSE 8300

CMD ["python", "./main.py"]