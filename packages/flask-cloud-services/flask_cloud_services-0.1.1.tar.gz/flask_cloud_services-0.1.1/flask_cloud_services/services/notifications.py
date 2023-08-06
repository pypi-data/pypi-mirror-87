from .. import config
from ..provider.factory import factory


def listener(func):
    """ Endpoint of Suscription and Reception of Notifications

    Implementation of `listener` of notifications bus
    for Flask. Already return response.
    The decorated function must not return anything.
    """

    def wrapper(*args, **kwargs):
        provider = factory('BusNotifications')
        result = provider.listener()
        if result.message_type == config.NOTIFICATION:
            func(data_listener=result, *args, **kwargs)
        return result.response
    wrapper.__doc__ = func.__doc__
    return wrapper


def publisher(
    topic_arn: str = None,
    message: str = None,
    *args,
    **kwargs
):
    """ Function to publication of Notifications

    Implementation of `publisher` of notifications bus

    Args:
        topic_arn (str): topic arn of channel
        message (str): message to publish
    """
    provider = factory('BusNotifications')
    return provider.publisher(
        topic_arn=topic_arn,
        message=message,
        *args,
        **kwargs
    )
