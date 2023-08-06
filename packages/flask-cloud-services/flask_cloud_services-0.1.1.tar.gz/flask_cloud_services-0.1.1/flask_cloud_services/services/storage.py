from ..provider.factory import factory


def upload_from_filename(
    filename: str,
    bucket_name: str,
    *args,
    **kwargs,
):
    """Function to upload file from given filename to cloud storage

    Implementation of `upload_from_filename` of Storage service

    Args:
        filename (str): The path to the file to upload.
        bucket_name (str): The name of the bucket to upload to.
        args
        kwargs

    Note: It accept any parameter the adapter needs,
        wich does not deliver in request
    """

    return factory('Storage').upload_from_filename(
        filename=filename,
        bucket_name=bucket_name,
        *args,
        **kwargs
    )


def upload_from_file_obj(
    file_obj,
    bucket_name: str,
    key: str,
    *args,
    **kwargs,
) -> None:
    """Function to upload file from given file object to cloud

    Args:
        file_obj (Object): The file object to upload by provider requirements.
        bucket_name (str): The name of the bucket to upload to.
        key (str): The file name in Cloud Storage. Default None
        extra_args (dict): Extra args. Default {}
        args
        kwargs

    Note: It accept any parameter the adapter needs,
            wich does not deliver in request
    """

    return factory('Storage').upload_from_file_obj(
        file_obj=file_obj,
        bucket_name=bucket_name,
        key=key,
        *args,
        **kwargs
    )


def download_from_filename(
    filename: str,
    bucket_name: str,
    key: str,
    *args,
    **kwargs,
):
    """Function to upload file from given filename to cloud storage

    Args:
        filename (str): The path to the file to download.
        bucket_name (str): The name of the bucket to download to.
        key (str): The file name to download to.
        args
        kwargs

    Note: It accept any parameter the adapter needs,
        wich does not deliver in request
    """

    return factory('Storage').download_from_filename(
        filename=filename,
        bucket_name=bucket_name,
        key=key,
        *args,
        **kwargs
    )


def get_file_url(
    bucket_name: str,
    key: str,
    *args,
    **kwargs,
) -> str:
    """Function to get file url from cloud storage

    Implementation of `get_file_url` from cloud storage

    Args:
        bucket_name (str): The name of the bucket to upload to.
        key (str): The file name in Cloud Storage.
        args
        kwargs

    Note: It accept any parameter the adapter needs,
        wich does not deliver in request

    Returns:
        str: URL file
    """
    return factory('Storage').get_file_url(
        bucket_name=bucket_name,
        key=key,
        *args,
        **kwargs
    )
