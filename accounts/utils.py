'''
'''
from django.conf import settings
from django.db.models import Q

from accounts.models import *

from pyapns.apns import APNs, Frame, Payload
from gcmclient import *

import datetime, time, pytz, sys


def filter_objects_by_user(user, model_class):
    if user.user_profiles.user_role == "super_admin":
        objects = model_class.objects \
                    .filter(
                        Q(user=user) |
                        Q(user__user_profiles__admin=user) |
                        Q(user__user_profiles__admin__user_profiles__admin=user)
                    )
    elif user.user_profiles.user_role == "admin":
        objects = model_class.objects \
                    .filter(
                        Q(user=user) |
                        Q(user__user_profiles__admin=user) |
                        Q(user__user_profiles__admin=user.user_profiles.admin)
                    )
    else:
        objects = model_class.objects.filter(user=user)
    return objects


def get_users(user):
    if user.user_profiles.user_role == "super_admin":
        users = User.objects \
                .filter(
                    Q(user_profiles__admin=user) |
                    Q(user_profiles__admin__user_profiles__admin=user)
                ) \
                .exclude(pk=user.id)
    else:
        users = User.objects \
                .filter(
                    Q(user_profiles__admin=user) |
                    Q(user_profiles__admin=user.user_profiles.admin)
                ) \
                .filter(user_profiles__user_role="employee") \
                .exclude(pk=user.id)

    return users


def send_android_notifications(title, message, reg_token):
    print "Sending Android Notification... %s", reg_token
    # Pass 'proxies' keyword argument, as described in 'requests' library if you
    # use proxies. Check other options too.
    gcm = GCM(settings.GCM_API_KEY)

    # Construct (key => scalar) payload. do not use nested structures.
    data = {'title':title, 'message':message}

    # Unicast or multicast message, read GCM manual about extra options.
    # It is probably a good idea to always use JSONMessage, even if you send
    # a notification to just 1 registration ID.
    unicast = PlainTextMessage(reg_token, data, dry_run=False)

    try:
        # attempt send
        res = gcm.send(unicast)

        # nothing to do on success
        for reg_id, msg_id in res.success.items():
            print "Successfully sent %s as %s" % (reg_id, msg_id)

        # update your registration ID's
        for reg_id, new_reg_id in res.canonical.items():
            print "Replacing %s with %s in database" % (reg_id, new_reg_id)

        # probably app was uninstalled
        for reg_id in res.not_registered:
            print "Removing %s from database" % reg_id

        # unrecoverably failed, these ID's will not be retried
        # consult GCM manual for all error codes
        for reg_id, err_code in res.failed.items():
            print "Removing %s because %s" % (reg_id, err_code)

        # if some registration ID's have recoverably failed
        if res.needs_retry():
            # construct new message with only failed regids
            retry_msg = res.retry()
            # you have to wait before attemting again. delay()
            # will tell you how long to wait depending on your
            # current retry counter, starting from 0.
            print "Wait or schedule task after %s seconds" % res.delay(retry)
            # retry += 1 and send retry_msg again

    except GCMAuthenticationError:
        # stop and fix your settings
        print "Your Google API key is rejected"
    except ValueError, e:
        # probably your extra options, such as time_to_live,
        # are invalid. Read error message for more info.
        print "Invalid message/option or invalid GCM response"
        print e.args[0]
    except Exception:
        # your network is down or maybe proxy settings
        # are broken. when problem is resolved, you can
        # retry the whole message.
        print "Something wrong with requests library"


def send_ios_notifications(message, reg_token):
    try:
        apns = APNs(use_sandbox=True, cert_file=settings.CERT_FILE,
                    key_file=settings.KEY_FILE)

        # Send a notification
        payload = Payload(alert=message, sound="default", badge=1)
        apns.gateway_server.send_notification(reg_token, payload)
    except:
        print "iOS Notification Error. %s", reg_token
        print sys.exc_info()