from datetime import timedelta
from django.utils import timezone
from celery import shared_task
from .models import OneTimeCode


@shared_task
def autodelete_one_time_codes():
    one_time_codes = OneTimeCode.objects.filter(create_datetime__lt=timezone.now() - timedelta(minutes=3))
    for one_time_code in one_time_codes:
        one_time_code.delete()

