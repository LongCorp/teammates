from decouple import config


db_data = {
    "host": 'localhost',
    "port": 3306,
    "user": 'root',
    "password": config("DB_PASSWORD"),
    "db": config("DB_NAME"),
    "autocommit": True
}

redis_config = {
    "url": "redis://localhost",
    "decode_responses": True,
    "encoding": "utf-8"
}

auth_service_url = config("AUTH_SERVICE_URL")
