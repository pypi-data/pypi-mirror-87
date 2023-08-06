import json
import logging
import requests
import boto3
from flask import request
from .. import config
from ..constants import responses as rsp
from ..config import NOTIFICATION, SUSCRIPTION
from ..contract import (
    BusNotificationsContract,
    StorageContract,
)
from ..contract import DataListener


__all__ = (
    'BusNotifications',
    'Storage',
)


class BusNotifications(BusNotificationsContract):

    def listener(self) -> DataListener:
        """Endpoint of Suscription and Reception of Notifications of AWS sns.
        Implementation of `listener` of AWS notifications bus
        for flask.

        Returns:
            ..contract.DataListener:
        """
        try:
            data = json.loads(request.data)
        except Exception as e:
            logging.error(str(e))
            return DataListener(
                response=(rsp.AWS_BAD_REQUEST, 400)
            )
        message_type = request.headers.get('X-Amz-Sns-Message-Type')
        topic_arn = request.headers.get('X-Amz-Sns-Topic-Arn')
        if message_type == 'Notification':
            # Receive notification from AWS channel and call decorated function
            result = DataListener(
                message_type=NOTIFICATION,
                message=data['Message'],
                topic_arn=topic_arn,
                response=rsp.AWS_OK,
            )
        elif (message_type == 'SubscriptionConfirmation'
                and 'SubscribeURL' in data):
            # Confirm suscription of AWS channel
            requests.get(data['SubscribeURL'])
            result = DataListener(
                message_type=SUSCRIPTION,
                topic_arn=topic_arn,
                response=rsp.AWS_OK
            )
        else:
            result = DataListener(
                response=(rsp.AWS_BAD_REQUEST, 400)
            )
        return result

    def publisher(
        self,
        topic_arn: str = None,
        message: str = None
    ) -> dict:
        """Method to publish in sns of AWS.
        Implementation of `publisher` to AWS notifications bus
        for Flask.

        Args:
            topic_arn (str)
            message (str)

        Returns:
            dict: Response returned by client sns
        """
        client = boto3.client(
            'sns',
            region_name=config.AWS_REGION,
            aws_access_key_id=config.AWS_ACCESS_KEY,
            aws_secret_access_key=config.AWS_SECRET_KEY,
        )
        # Publish a simple message to the specified SNS topic
        return client.publish(
            TopicArn=topic_arn,
            Message=message
        )


class Storage(StorageContract):

    CLIENT = boto3.client(
        's3',
        region_name=config.AWS_REGION,
        aws_access_key_id=config.AWS_ACCESS_KEY,
        aws_secret_access_key=config.AWS_SECRET_KEY,
    )

    def upload_from_filename(
        self,
        filename: str,
        bucket_name: str,
        key: str,
        extra_args: str = {},
        *args,
        **kwargs,
    ) -> None:
        """Function to upload file from given filename to S3

        Implementation of `upload_from_filename` using S3

        Args:
            filename (str): The path to the file to upload.
            bucket_name (str): The name of the bucket to upload to.
            key (str): The file name in Cloud Storage. Default None
            extra_args (dict): Extra args. Default {}
            args
            kwargs

        Note: It accept any parameter the adapter needs,
                wich does not deliver in request
        """

        return self.CLIENT.upload_file(
            Filename=filename,
            Bucket=bucket_name,
            Key=key,
            ExtraArgs=extra_args,
            *args,
            **kwargs
        )

    def upload_from_file_obj(
        self,
        file_obj: str,
        bucket_name: str,
        key: str,
        extra_args: str = {},
        *args,
        **kwargs,
    ) -> None:
        """Function to upload file from given file object to S3

        Implementation of `upload_fileobj` using S3

        Args:
            file_obj (Object): The file object to upload by S3 requirements.
            bucket_name (str): The name of the bucket to upload to.
            key (str): The file name in Cloud Storage. Default None
            extra_args (dict): Extra args. Default {}
            args
            kwargs

        Note: It accept any parameter the adapter needs,
                wich does not deliver in request
        """

        return self.CLIENT.upload_fileobj(
            Fileobj=file_obj,
            Bucket=bucket_name,
            Key=key,
            ExtraArgs=extra_args,
            *args,
            **kwargs
        )

    def download_from_filename(
        self,
        filename: str,
        bucket_name: str,
        key: str,
        extra_args: str = {},
        *args,
        **kwargs,
    ) -> None:
        """Function to download file from given filename to S3

        Implementation of `download_file` using S3

        Args:
            filename (str): The path to the file to upload.
            bucket_name (str): The name of the bucket to upload to.
            key (str): The file name in Cloud Storage.
            args
            kwargs

        Note: It accept any parameter the adapter needs,
            wich does not deliver in request
        """
        return self.CLIENT.download_file(
            Bucket=bucket_name,
            Key=key,
            Filename=filename,
            ExtraArgs=extra_args,
            *args,
            **kwargs
        )

    def get_file_url(
        self,
        bucket_name: str,
        key: str,
        *args,
        **kwargs,
    ) -> str:
        """Function to get file url

        Implementation of `get_file_url` using S3

        Args:
            bucket_name (str): The name of the bucket to upload to.
            key (str): The file name in Cloud Storage.
            args
            kwargs

        Note: It accept any parameter the adapter needs,
            wich does not deliver in request

        Returns:
            str: URL built
        """
        bucket_location = self.CLIENT.get_bucket_location(Bucket=bucket_name)
        bucket_location = bucket_location['LocationConstraint']
        _ = f"https://s3-{bucket_location}.amazonaws.com/{bucket_name}/{key}"
        return _
