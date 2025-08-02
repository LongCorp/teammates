from decouple import config


CHAT_DB_URL = f"mysql+aiomysql://{config('CHAT_DB_USER')}:{config('CHAT_DB_PASSWORD')}@{config('CHAT_DB_HOST')}:{config('CHAT_DB_PORT')}/{config('CHAT_DB_NAME')}"

MAIN_DB_URL = f"mysql+aiomysql://{config('DB_USER')}:{config('DB_PASSWORD')}@{config('DB_HOST')}:{config('DB_PORT')}/{config('DB_NAME')}"

auth_service_url = config('AUTH_SERVICE_URL')