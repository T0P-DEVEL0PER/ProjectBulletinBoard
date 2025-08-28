from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import *


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


@receiver(post_save, sender=Reply)
def send_one_time_code(instance, created, **kwargs):
    if created:
        send_mail(
            subject='ProjectBulletinBoard',
            message='',
            from_email='igreatprojectsi@yandex.ru',
            recipient_list=[instance.advertisement.user.email],
            html_message=f"""
                <h1>На Ваше объявление {instance.advertisement.title} откликнулись!</h1>
                <p>{instance.advertisement.user.username},</p>
                <p>На Ваше объявление {instance.advertisement.title} откликнулся {instance.user.username}.</p>
                <button><a href="http://127.0.0.1:8000/your_advertisements/{instance.advertisement.pk}/replies/{instance.pk}">Просмотр</a></button>
            """,
        )
    else:
        if instance.is_accepted:
            send_mail(
                subject='ProjectBulletinBoard',
                message='',
                from_email='igreatprojectsi@yandex.ru',
                recipient_list=[instance.user.email],
                html_message=f"""
                    <h1>Ваш отклик на объявление {instance.advertisement.title} принят!</h1>
                    <p>{instance.advertisement.user.username},</p>
                    <p>Ваш отклик на объявление {instance.advertisement.title}, созданное пользователем {instance.advertisement.user.username}, принят.</p>
                    <button><a href="http://127.0.0.1:8000/your_advertisements/{instance.advertisement.pk}/replies/{instance.pk}">Просмотр</a></button>
                """,
            )
        else:
            send_mail(
                subject='ProjectBulletinBoard',
                message='',
                from_email='igreatprojectsi@yandex.ru',
                recipient_list=[instance.advertisement.user.email],
                html_message=f"""
                    <h1>Отклик на Ваше объявление {instance.advertisement.title} изменён!</h1>
                    <p>{instance.advertisement.user.username},</p>
                    <p>Отклик пользователя {instance.user.username} на Ваше объявление {instance.advertisement.title} был изменён.</p>
                    <button><a href="http://127.0.0.1:8000/your_advertisements/{instance.advertisement.pk}/replies/{instance.pk}">Просмотр</a></button>
                """,
            )
