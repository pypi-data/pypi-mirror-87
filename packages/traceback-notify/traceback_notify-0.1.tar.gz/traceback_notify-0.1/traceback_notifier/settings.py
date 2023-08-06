import os

SENDGRID_API_TOKEN = os.environ.get('SENDGRID_API_TOKEN')
EMAIL_FROM = os.environ.get('EMAIL_FROM')
SEND_TO = os.environ.get('SEND_TO', '').split(',')
SCOPE = os.environ.get('SCOPE')
