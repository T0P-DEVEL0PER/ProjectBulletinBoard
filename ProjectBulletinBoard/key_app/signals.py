from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import OneTimeCode


@receiver(post_save, sender=OneTimeCode)
def send_one_time_code(instance, created, **kwargs):
    if created:
        if instance.user.is_active:
            send_mail(
                subject='ProjectBulletinBoard',
                message='',
                from_email='igreatprojectsi@yandex.ru',
                recipient_list=[instance.user.email],
                html_message=f"""
                    <h1>Ваш код - {instance.symbols}</h1>
                    <p>{instance.user.username},</p>
                    <p>Ваш код: {instance.symbols}. Его можно использовать для входа.</p>
                    <p>Если вы не запрашивали это сообщение, проигнорируйте его.</p>
                    <p>Код действителен 3 минуты, в течение которых Вы не можете запрашивать новый код.</p>
                """,
            )
        if not instance.user.is_active:
            send_mail(
                subject='ProjectBulletinBoard',
                message='',
                from_email='igreatprojectsi@yandex.ru',
                recipient_list=[instance.user.email],
                html_message=f"""
                    <h1>Ваш код - {instance.symbols}</h1>
                    <p>{instance.user.username},</p>
                    <p>Ваш код: {instance.symbols}. Его можно использовать для подтверждения регистрации.</p>
                    <p>Если вы не запрашивали это сообщение, проигнорируйте его.</p>
                    <p>Код действителен 3 минуты, в течение которых Вы не можете запрашивать новый код.</p>
                """,
            )
