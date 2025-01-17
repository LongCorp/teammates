from decouple import config


db_data = {
    "host": config("DB_HOST"),
    "port": 3306,
    "user": 'root',
    "password": config("DB_PASSWORD"),
    "db": config("DB_NAME"),
    "autocommit": True
}

auth_service_url = config("AUTH_SERVICE_URL")