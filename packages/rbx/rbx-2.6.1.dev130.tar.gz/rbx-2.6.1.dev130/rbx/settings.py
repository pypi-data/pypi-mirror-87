import os
import google.auth

RBX_ENV = os.getenv('RBX_ENV', 'dev')
RBX_PROJECT = f'{RBX_ENV}-platform-eu'

# Google Cloud Platform
# Fail immediately when GCP authentication fails
GOOGLE_CREDENTIALS, GOOGLE_PROJECT = google.auth.default()
GOOGLE_PUBSUB_TOPIC = os.getenv('GOOGLE_PUBSUB_TOPIC', "platform-notifications")
GOOGLE_PUBSUB_PAYLOAD_VERSION = 2
