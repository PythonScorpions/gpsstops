'''
'''
from django.conf import settings
from django_cron import CronJobBase, Schedule
from django.template import loader, Context
from django.core.mail import send_mail

from pyapns.apns import APNs, Frame, Payload

# from push_notifications.models import GCMDevice

from appointments.models import *
from accounts.models import *

from gcmclient import *

import datetime, time, pytz, sys


class NotificationsCronJob(CronJobBase):
    RUN_EVERY_MINS = 5 # every 2 hours

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'appointments.notifications_cron_job'    # a unique code

    def do(self):
        try:
            print "reached....%s IST" % datetime.datetime.now(pytz.timezone('Asia/Calcutta'))
            self._send_appointments_notifications()
            self._send_tasks_notifications()
        except:
            print "Fatal Error: ", sys.exc_info()

    def _send_ios_notifications(self, message, reg_token):
        try:
            apns = APNs(use_sandbox=True, cert_file=settings.CERT_FILE, key_file=settings.KEY_FILE)

            # Send a notification
            payload = Payload(alert=message, sound="default", badge=1)
            apns.gateway_server.send_notification(reg_token, payload)
        except:
            print "iOS Notification Error. %s", reg_token
            print sys.exc_info()

    def _send_android_notifications(self, title, message, reg_token):
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

    def _check_date(self, dt_to_be_checked, given_timezone, notification_time):
        try:
            cur_dt = datetime.datetime.now(pytz.timezone(given_timezone))
        except:
            print sys.exc_info()
        else:
            cur_dt_in_secs = time.mktime(cur_dt.timetuple())
            given_dt_in_secs = time.mktime(dt_to_be_checked.timetuple())

            if (given_dt_in_secs - cur_dt_in_secs) <= (notification_time * 60):
                print "Dates matched."
                return True
            else:
                print "Dates not matched."
        return False

    def _send_email(self, template, context, title, email):
        template = loader.get_template(template)
        context = Context(context)
        print "Sending email...", settings.EMAIL_HOST_USER, email
        send_mail(title, template.render(context),
            settings.EMAIL_HOST_USER, [str(email)], fail_silently=False)

    def _send_appointment_email(self, appointment):
        print "Sending Appointment Email...."
        self._send_email('email/appointments.email', {'appointment':appointment},
            'Appointment Notification', appointment.user.email)
        AppointmentEmailNotification.objects \
        .create(appointment=appointment, flag=True)

    def _send_task_email(self, task):
        print "Sending Task Email...."
        self._send_email('email/task.email', {'task':task},
            'Task Notification', task.user.email)
        TaskEmailNotification.objects \
        .create(task=task, flag=True)

    def _send_appointments_notifications(self):
        ''' Send notifications for all appointments '''
        appointments = Appointments.objects \
                        .exclude(appointmentnotification__flag=True)
        for appointment in appointments:
            print "checking notification appointment.....", appointment.id, appointment.title
            if not appointment.notification_required:
                print "....notification not required."
                continue

            if not self._check_date(
                        appointment.start_datetime,
                        appointment.timezone,
                        appointment.notification_time):
                continue

            email_flag = False
            try:
                email_notification = AppointmentEmailNotification.objects \
                                    .get(appointment=appointment)
            except:
                print sys.exc_info()
                email_flag = True
            else:
                email_flag = not email_notification.flag
            if email_flag:
                self._send_appointment_email(appointment)

            try:
                notification = AppointmentNotification.objects \
                                .get(appointment=appointment)
            except:
                print sys.exc_info()
            else:
                if notification.flag:
                    continue

            print "Checking device...."
            try:
                devices = RegistratedDevice.objects.filter(user=appointment.user)
            except:
                print sys.exc_info()
            else:
                for device in devices:
                    message = "Appointment: %s, %s" % (appointment.title,
                                appointment.start_datetime)
                    print "Sending %s to device type %s" % (message, device.device_type)
                    if device.device_type.lower() == 'ios':
                        self._send_ios_notifications(message,
                                device.device_token)
                        AppointmentNotification.objects \
                        .create(appointment=appointment, flag=True)
                    elif device.device_type.lower() == 'android':
                        self._send_android_notifications('Appointment', message,
                            device.device_token)
                        AppointmentNotification.objects \
                        .create(appointment=appointment, flag=True)
                    else:
                        print "Device type not found. Device: %s.... Appointment: %s" % (
                            device.device_type, appointment.id)

    def _send_tasks_notifications(self):
        ''' Send tasks for all appointments '''
        tasks = Task.objects.exclude(tasknotification__flag=True)
        for task in tasks:
            print "checking notification task.....", task.id, task.title
            if not task.notification_required:
                print "....notification not required."
                continue

            if not self._check_date(
                        task.due_date,
                        task.timezone,
                        task.notification_time):
                continue

            email_flag = False
            try:
                email_notification = TaskEmailNotification.objects \
                                     .get(task=task)
            except:
                print sys.exc_info()
                email_flag = True
            else:
                email_flag = not email_notification.flag

            print "Task email flag: ", email_flag
            if email_flag:
                self._send_task_email(task)

            try:
                notification = TaskNotification.objects.get(task=task)
            except:
                print sys.exc_info()
            else:
                if notification.flag:
                    continue

            print "Checking device...."
            try:
                devices = RegistratedDevice.objects.filter(user=task.user)
            except:
                print sys.exc_info()
            else:
                for device in devices:
                    message = "Task: %s, %s" % (task.title, task.due_date)
                    print "Sending %s to device type %s" % (message, device.device_type)
                    if device.device_type.lower() == 'ios':
                        self._send_ios_notifications(message,
                                device.device_token)
                        TaskNotification.objects.create(task=task, flag=True)
                    elif device.device_type.lower() == 'android':
                        self._send_android_notifications('Task', message,
                            device.device_token)
                        TaskNotification.objects.create(task=task, flag=True)
                    else:
                        print "Device type not found. Device: %s.... Task: %s" % (
                            device.device_type, task.id)
