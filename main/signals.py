from django.contrib.auth import user_logged_in, user_logged_out
from django.dispatch import receiver
from main.models import UserSession


@receiver(user_logged_in)
def on_user_logged_in(sender, **kwargs):
    UserSession.objects.get_or_create(user=kwargs.get('user'))


@receiver(user_logged_out)
def on_user_logged_out(sender, **kwargs):
    UserSession.objects.filter(user=kwargs.get('user')).delete()
