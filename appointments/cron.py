'''
'''
from django.conf import settings

from django_cron import CronJobBase, Schedule

from pyapns.apns import APNs, Frame, Payload

from push_notifications.models import GCMDevice

from appointments.models import *
from accounts.models import *

import datetime, pytz, sys


class NotificationsCronJob(CronJobBase):
    RUN_EVERY_MINS = 5 # every 2 hours

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'appointments.notifications_cron_job'    # a unique code

    def do(self):
        try:
            print "reached....", datetime.datetime.now()
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

    def _send_android_notifications(self, message, reg_token):
        try:
            device = GCMDevice.objects.get(registration_id=gcm_reg_id)
            # The first argument will be sent as "message" to the intent extras Bundle
            # Retrieve it with intent.getExtras().getString("message")
            device.send_message(message)
        except:
            print "Android Notification Error. %s", reg_token
            print sys.exc_info()

    def _check_date(date_to_be_checked, given_timezone):
        cur_date = datetime.datetime.now(pytz.timezone(given_timezone)).date()
        if date_to_be_checked == cur_date:
            return True
        return False

    def _send_appointments_notifications(self):
        ''' Send notifications for all appointments '''
        appointments = Appointments.objects \
                        .exclude(appointmentnotification__flag=True)
        for appointment in appointments:
            print "Sending notification appointment.....", appointment.id, appointment.title
            if not self._check_date(appointment.start_datetime.date(),
                        appointment.timezone):
                continue

            try:
                notification = AppointmentNotification.objects \
                                .get(appointment=appointment)
            except:
                pass
            else:
                if notification.flag:
                    continue

            print "Checking device...."
            try:
                device = RegistratedDevice.objects \
                            .get(user=appointment.user)
            except:
                pass
            else:
                message = "Appointment: %s, %s" % (appointment.title,
                            appointment.start_datetime)
                print message
                if device.device_type.lower() == 'ios':
                    self._send_ios_notifications(message,
                            device.device_token)
                    AppointmentNotification.objects \
                    .create(appointment=appointment, flag=True)
                elif device.device_type.lower() == 'android':
                    # self._send_android_notifications(message,
                    #     device.device_token)
                    # AppointmentNotification.objects \
                    # .create(appointment=appointment, flag=True)
                    pass
                else:
                    print "Device type not found. Device: %s.... Appointment: %s" % (
                        device.device_type, appointment.id)

    def _send_tasks_notifications(self):
        ''' Send tasks for all appointments '''
        tasks = Task.objects \
                .exclude(tasknotification__flag=True)
        for task in tasks:
            print "Sending notification task.....", task.id, task.title
            if not self._check_date(appointment.start_datetime.date(),
                        task.timezone):
                continue

            try:
                notification = TaskNotification.objects \
                                .get(appointment=appointment)
            except:
                pass
            else:
                if notification.flag:
                    continue

            print "Checking device...."
            try:
                device = RegistratedDevice.objects.get(user=task.user)
            except:
                pass
            else:
                message = "Task: %s, %s" % (task.title, task.start_datetime)
                print message
                if device.device_type.lower() == 'ios':
                    self._send_ios_notifications(message,
                            device.device_token)
                    TaskNotification.objects.create(task=task, flag=True)
                elif device.device_type.lower() == 'android':
                    self._send_android_notifications(message,
                        device.device_token)
                    TaskNotification.objects.create(task=task, flag=True)
                else:
                    print "Device type not found. Device: %s.... Task: %s" % (
                        device.device_type, task.id)