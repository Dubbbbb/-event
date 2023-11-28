from celery import shared_task

from .models import Notification


@shared_task
def create_invite_notification(users, event_name):
    message = f'You were invited to - <b>{event_name}</b>'
    for user in users:
        new_notif = Notification.objects.create(message=message, user=user, type='invite')
        new_notif.save()


def create_uninvite_notification(user_id, event_name):
    message = f'You were removed from - <b>{event_name}</b>'
    new_notif = Notification.objects.create(message=message, user_id=user_id, type='uninvite')
    new_notif.save()
