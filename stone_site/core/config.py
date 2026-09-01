from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Base
    DB_HOST: str 
    DB_PORT: int 
    DB_USER: str 
    DB_PASS: str
    DB_NAME: str
    # JWT
    SECRET_KEY: str 
    ALGORITHM: str 
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    # S3
    S3_ENDPOINT: str = "localhost:9000"           # Адрес S3 сервера
    S3_ACCESS_KEY: str = "minioadmin"             # Ключ доступа
    S3_SECRET_KEY: str = "minioadmin"             # Секретный ключ       # Основной бакет
    S3_IMAGES_BUCKET: str = "stone-site-images"   # Бакет для изображений
    S3_USE_SSL: bool = False                      # Использовать ли HTTPS (в локальной разработке false)
    # RabbitMQ
    RABBITMQ_URL: str = "amqp://guest:guest@rabbitmq:5672/"
    # MailHog
    MAIL_SERVER: str = "mailhog"
    MAIL_PORT: int = 1025
    MAIL_USERNAME: str = ""
    MAIL_PASSWORD: str = ""
    MAIL_USE_TLS: bool = False
    MAIL_USE_SSL: bool = False
    MAIL_FROM_EMAIL: str = "noreply@stone-site.com"

    @property
    def DATABASE_URL(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    
    class Config:
        env_file=".env"
        env_file_encoding = "utf-8"
        case_sesnsitive = True
    
settings = Settings()