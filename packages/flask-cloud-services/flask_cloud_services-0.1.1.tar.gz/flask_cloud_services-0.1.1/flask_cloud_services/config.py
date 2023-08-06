import os

PROVIDER = os.environ.get('CLOUD_SERVICES_PROVIDER')

# AWS Config
AWS_REGION = os.environ.get('CLOUD_SERVICES_AWS_REGION')
AWS_ACCESS_KEY = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')

# Notification Bus services
NOTIFICATION = 'Notification'
SUSCRIPTION = 'Subscription'
