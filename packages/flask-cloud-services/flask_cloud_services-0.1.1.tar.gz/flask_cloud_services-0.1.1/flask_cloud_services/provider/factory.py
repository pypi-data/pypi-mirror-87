from .. import config
from . import aws

providers = {
    'aws': aws
}


def factory(service: str):
    """Call the provider available selected from config.PROVIDER

    Returns:
        class: provider instanced
    """
    if config.PROVIDER not in providers:
        raise Exception(f'Provider {config.PROVIDER} is not available')
    provider = providers[config.PROVIDER]
    if service not in provider.__all__:
        raise Exception(
            'Service {} is not available '
            'for Provider {}'.format(service, config.PROVIDER)
        )
    return getattr(provider, service)()
