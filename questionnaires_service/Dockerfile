FROM python:3.11-alpine
LABEL authors="decobraz"

WORKDIR /questionnaires_service

COPY . .

RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["python", "./main.py"]