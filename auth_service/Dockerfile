FROM python:3.11-alpine
LABEL authors="decobraz"

WORKDIR /auth_service

COPY . .

RUN pip install -r requirements.txt

EXPOSE 8100

CMD ["python", "./main.py"]