from django.template.loader import render_to_string
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode

from .tasks import email_sender


def token_validator(token):
    from .models import User
    email = force_str(urlsafe_base64_decode(token))
    user = User.objects.get(email=email)
    if user.is_active:
        raise Exception

    return user


def email_message_generator(user, template):
    message = render_to_string(f'{template}', {
        'user': user,
        'token': user.link,
    })

    return message


def send_email(user, subject, template):
    message = email_message_generator(user, template)
    email_sender.delay(message, user.email, subject)

