import asyncio
import io
import json
import uuid
from functools import partial

from minio import Minio

from app.core.config import Settings
from app.core.services.i_storage_service import IStorageService


class MinioStorageService(IStorageService):
    def __init__(self, settings: Settings):
        self._client = Minio(
            settings.MINIO_ENDPOINT,
            access_key=settings.MINIO_ACCESS_KEY,
            secret_key=settings.MINIO_SECRET_KEY,
            secure=settings.MINIO_SECURE,
        )
        self._bucket = settings.MINIO_BUCKET
        self._public_url_base = settings.MINIO_PUBLIC_URL_BASE

    def _public_policy(self) -> str:
        return json.dumps({
            "Version": "2012-10-17",
            "Statement": [{
                "Effect": "Allow",
                "Principal": {"AWS": ["*"]},
                "Action": ["s3:GetObject"],
                "Resource": [f"arn:aws:s3:::{self._bucket}/*"],
            }],
        })

    def ensure_bucket_exists(self) -> None:
        if not self._client.bucket_exists(self._bucket):
            self._client.make_bucket(self._bucket)
        self._client.set_bucket_policy(self._bucket, self._public_policy())

    async def upload_image(self, data: bytes, filename: str, content_type: str) -> str:
        ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else "jpg"
        object_name = f"{uuid.uuid4().hex}.{ext}"

        loop = asyncio.get_running_loop()
        await loop.run_in_executor(
            None,
            partial(
                self._client.put_object,
                self._bucket,
                object_name,
                io.BytesIO(data),
                len(data),
                content_type=content_type,
            ),
        )
        return f"{self._public_url_base}/{object_name}"
