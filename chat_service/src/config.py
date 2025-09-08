from decouple import config



MAIN_DB_URL = f"mysql+aiomysql://{config('DB_USER')}:{config('DB_PASSWORD')}@{config('DB_HOST')}:{config('DB_PORT')}/{config('DB_NAME')}"

auth_service_url = config('AUTH_SERVICE_URL')