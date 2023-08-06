# Cloud Services

PIP package to provide cloud services.

## Package installation
- Installation
    ```shell
    $ pip3 install flask-cloud-services
    ```

## Configuration

Define the following environment variables:

* (str) Provider. Allowed: [aws, ]

        CLOUD_SERVICES_PROVIDER=

Aws Config

* (str) Region. Example: 'us-west-2'

        CLOUD_SERVICES_AWS_REGION=

* (str) Credentials: Access Key.

        AWS_ACCESS_KEY_ID=

* (str) Credentials: Secret Key.

        AWS_SECRET_ACCESS_KEY=

## How to use

### AWS Services

#### Notifications Channel

##### Subscribe and Listen Notifications

Define your route where you want listen the Notification Channel and you decorate it.

```python
from flask import Blueprint
from flask_cloud_services import notifications_listener

routes_bus = Blueprint('routes_bus', __name__)

@routes_bus.route('/notification-channel', methods=['GET', 'POST', 'PUT'])
@notifications_listener
def aws_sns(data_listener):
    any_topic_arn = "arn:aws:sns:us-west-2:test:test"
    if data_listener.topic_arn == any_topic_arn:
        pass # DO SOMETHING
```

##### Publish Events

If you want publish an event to specific channel,
you just must call the function `publish` send it
`topic_arn` and `message` encoded.

```python
from flask_cloud_services import notifications_publisher

result = notifications_publisher(
    topic_arn="arn:aws:sns:us-west-2:test:test",
    message="{\"data\": \"value\"}"
)
```