import abc


class DataListener:
    """Object used for BusNotifications.listener()

    Attributes:
        message: type unknown
        response: type unknown
    """

    def __init__(
        self,
        message_type: str = None,
        topic_arn: str = None,
        message=None,
        response=None
    ):
        self.message_type = message_type
        self.topic_arn = topic_arn
        self.message = message
        self.response = response


class BusNotificationsContract(metaclass=abc.ABCMeta):
    """Contract for Notification service"""

    @abc.abstractmethod
    def listener(self) -> DataListener:
        """It must Subscribe or Receive Notifications from Notifications Bus
        Implementation of `listener` of Notifications Bus

        Returns:
            DataListener:
        """
        pass

    @abc.abstractmethod
    def publisher(
        self,
        topic_arn: str,
        message: str,
        *args,
        **kwargs,
    ):
        """It must Publish to Notifications Bus

        Args:
            topic_arn (str): topic arn of channel
            message (str): message to publish

        Note: It accepts any parameter the adapter needs,
            wich does not deliver in request
        """
        pass


class StorageContract(metaclass=abc.ABCMeta):
    """Contract for Storage service"""

    @abc.abstractmethod
    def upload_from_filename(
        self,
        filename: str,
        bucket_name: str,
        *args,
        **kwargs,
    ):
        """It upload a file from file-like path.

        Args:

            filename (str): The path to the file to upload.
            bucket_name (str): The name of the bucket to upload to.
            args
            kwargs

        Note: It accepts any parameter the adapter needs,
            wich does not deliver in request
        """
        pass

    @abc.abstractmethod
    def upload_from_file_obj(
        self,
        file_obj,
        bucket_name: str,
        *args,
        **kwargs,
    ):
        """It upload a file from file-like object.

        Args:

            file_obj (Object): The file object to upload by
                provider requirements.
            bucket_name (str): The name of the bucket to upload to.
            args
            kwargs

        Note: It accepts any parameter the adapter needs,
            wich does not deliver in request
        """
        pass

    @abc.abstractmethod
    def download_from_filename(
        self,
        filename: str,
        bucket_name: str,
        key: str,
        *args,
        **kwargs,
    ):
        """Function to download file from given filename.

        Args:
            filename (str): The path to the file to download to.
            bucket_name (str): The name of the bucket to download to.
            key (str): The file name in Cloud Storage.
            args
            kwargs

        Note: It accepts any parameter the adapter needs,
                wich does not deliver in request
        """
        pass

    @abc.abstractmethod
    def get_file_url(
        self,
        bucket_name: str,
        key: str,
        *args,
        **kwargs,
    ):
        """Function to get file url from given key.

        Args:
            bucket_name (str): The name of the bucket.
            key (str): The file name in Cloud Storage.
            args
            kwargs

        Note: It accepts any parameter the adapter needs,
            wich does not deliver in request
        """
        pass
