import os
import posixpath
from mimetypes import guess_type

import boto3
from mlflow.utils.file_utils import relative_path_to_artifact_path

from .model_definition import ModelDefinition


class S3Util:
    @staticmethod
    def download_folder(local_dir, model_definition: ModelDefinition):
        s3 = boto3.resource(
            "s3",
            aws_access_key_id=model_definition.credentials.access_key_id,
            aws_secret_access_key=model_definition.credentials.secret_access_key,
        )
        bucket = s3.Bucket(model_definition.s3_path.bucket)
        for obj in bucket.objects.filter(Prefix=model_definition.s3_path.key):
            target = (
                obj.key
                if local_dir is None
                else os.path.join(
                    local_dir, os.path.relpath(obj.key, model_definition.s3_path.key)
                )
            )
            if not os.path.exists(os.path.dirname(target)):
                os.makedirs(os.path.dirname(target))
            if obj.key[-1] == "/":
                continue
            bucket.download_file(obj.key, target)

    @staticmethod
    def upload_folder(local_dir, model_definition: ModelDefinition):
        s3_client = boto3.client(
            "s3",
            aws_access_key_id=model_definition.credentials.access_key_id,
            aws_secret_access_key=model_definition.credentials.secret_access_key,
        )
        dest_path = model_definition.s3_path.key
        local_dir = os.path.abspath(local_dir)
        for (root, _, filenames) in os.walk(local_dir):
            upload_path = dest_path
            if root != local_dir:
                rel_path = os.path.relpath(root, local_dir)
                rel_path = relative_path_to_artifact_path(rel_path)
                upload_path = posixpath.join(dest_path, rel_path)
            for f in filenames:
                S3Util._upload_file(
                    s3_client=s3_client,
                    local_file=os.path.join(root, f),
                    bucket=model_definition.s3_path.bucket,
                    key=posixpath.join(upload_path, f),
                )

    @staticmethod
    def _upload_file(s3_client, local_file, bucket, key):
        extra_args = {}
        guessed_type, guessed_encoding = guess_type(local_file)
        if guessed_type is not None:
            extra_args["ContentType"] = guessed_type
        if guessed_encoding is not None:
            extra_args["ContentEncoding"] = guessed_encoding
        s3_client.upload_file(
            Filename=local_file, Bucket=bucket, Key=key, ExtraArgs=extra_args
        )
