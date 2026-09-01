import boto3  # Библиотека для работы с S3 (совместима с MinIO)
from botocore.exceptions import ClientError  # Ошибки S3
from typing import Optional
from .config import settings  

class S3Client:
    def __init__(self):
        self.endpoint = settings.S3_ENDPOINT
        self.access_key = settings.S3_ACCESS_KEY
        self.secret_key = settings.S3_SECRET_KEY
        self.images_bucket = settings.S3_IMAGES_BUCKET
        self.use_ssl = settings.S3_USE_SSL
        
        self.client = boto3.client("s3", 
            endpoint_url=f"{'https' if self.use_ssl else 'http'}://{self.endpoint}",
            aws_access_key_id=self.access_key,  # Логин
            aws_secret_access_key=self.secret_key,  # Пароль
            region_name="us-east-1",  # Регион (для MinIO не важно)
        )
    
    def upload_file(
            self, 
            file_data: bytes, 
            filename:str, 
            content_type: str = "image/jpeg") -> str:
        
        #     Как работает:
        # 1. Принимает байты файла и имя
        # 2. Загружает в S3 через put_object
        # 3. Возвращает URL для доступа к файлу

        try:
            self.client.put_object(
                Bucket=self.images_bucket,
                Key=filename,
                Body=file_data,
                ContentType=content_type
                )
            protocol = "https" if self.use_ssl else "http"
            return f"{protocol}://{self.endpoint}/{self.images_bucket}/{filename}"
        
        except ClientError as e:
            raise Exception(f"Error download file in S3: {e}")
        
# СОЗДАЕМ ОДИН ЭКЗЕМПЛЯР КЛИЕНТА ДЛЯ ВСЕГО ПРИЛОЖЕНИЯ
# Это называется "синглтон" - один объект на все приложение
s3_client = S3Client()