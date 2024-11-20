from decouple import config


db_data = {
    "host": 'localhost',
    "port": 3306,
    "user": 'root',
    "password": config("DB_PASSWORD"),
    "db": config("DB_NAME"),
    "autocommit": True
}
