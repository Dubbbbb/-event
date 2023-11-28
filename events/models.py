from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class TodoList(models.Model):
    pass


class PriceList(models.Model):
    pass


class TodoListTask(models.Model):
    text = models.CharField(max_length=256)
    status = models.BooleanField(default=False)
    todo_list = models.ForeignKey(TodoList, on_delete=models.CASCADE, related_name='tasks')


class PriceListItem(models.Model):
    name = models.CharField(max_length=256)
    price = models.FloatField()
    price_list = models.ForeignKey(PriceList, on_delete=models.CASCADE, related_name='items')


class Event(models.Model):
    title = models.CharField(max_length=128)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    users = models.ManyToManyField(User, related_name='invited_users', blank=True)
    todo_list = models.ForeignKey(TodoList, on_delete=models.CASCADE)
    price_list = models.ForeignKey(PriceList, on_delete=models.CASCADE)
    is_public = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.todo_list = TodoList.objects.create()
            self.price_list = PriceList.objects.create()
        super(Event, self).save(*args, **kwargs)


class Notification(models.Model):
    message = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notification')
    checked = models.BooleanField(default=False)
    type = models.CharField(max_length=64)
    created_at = models.DateTimeField(auto_now_add=True)
