from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Advertisement(models.Model):
    title = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    content = models.TextField()
    create_datetime = models.DateTimeField(auto_now_add=True)
    last_change_datetime = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Reply(models.Model):
    advertisement = models.ForeignKey(Advertisement, on_delete=models.CASCADE)
    text = models.TextField()
    is_accepted = models.BooleanField(default=False)
    create_datetime = models.DateTimeField(auto_now_add=True)
    last_change_datetime = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return 'Отклик на объявление ' + '"' + self.advertisement.title + '"'


class OneTimeCode(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    symbols = models.CharField(max_length=6)
    create_datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.symbols