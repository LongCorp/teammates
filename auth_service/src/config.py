from decouple import config


JWT_SECRET = config('JWT_SECRET')
PASSWORD_SALT = config('PASSWORD_SALT')

DATABASE_URL = f"mysql+aiomysql://{config('DB_USER')}:{config('DB_PASSWORD')}@{config('DB_HOST')}:{config('DB_PORT')}/{config('DB_NAME')}"
