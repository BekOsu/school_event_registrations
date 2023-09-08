from celery import shared_task
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import EmailMessage
from django.template.loader import get_template


@shared_task
def send_event_registration_email(user_id, event_name):
    user_instance = get_user_model().objects.get(pk=user_id)

    subject = f'You have been registered for {event_name}'
    message_template = get_template("event_registration_body.html")
    html_content = message_template.render({
        'user': user_instance.username,
        'event_name': event_name
    })
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [user_instance.email, ]
    reply_to = [settings.EMAIL_ADMIN]
    email = EmailMessage(
        subject,
        html_content,
        email_from,
        recipient_list,
        reply_to=reply_to,
    )
    email.content_subtype = "html"

    return email.send()
