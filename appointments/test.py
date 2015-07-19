'''
'''
import time
from pyapns.apns import APNs, Frame, Payload

from django.conf import settings

def test_ios():
    # apns = APNs(use_sandbox=True, cert_file=settings.PUSH_NOTIFICATIONS_SETTINGS['APNS_CERTIFICATE']) #, key_file='key.pem')
    apns = APNs(use_sandbox=True, cert_file=settings.CERT_FILE, key_file=settings.KEY_FILE)

    # Send a notification
    token_hex = 'c0710730ba72da45175ee571184eaa88103c58f6993bd321b252ed124714fad3'
    payload = Payload(alert="Hello World!", sound="default", badge=1)
    apns.gateway_server.send_notification(token_hex, payload)