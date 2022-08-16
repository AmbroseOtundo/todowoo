from django.contrib.auth.models import User
from django.db import models

class Todo(models.Model):
    title = models.CharField(max_length=100)
    # blank specifies its not a must to write a memo
    memo = models.TextField(blank=True)
    # grab created date
    created = models.DateTimeField(auto_now_add=True)
    datecompleted = models.DateTimeField(null=True)
    important = models.BooleanField(default=True)
    # know which todo belongs to who
    user = models.ForeignKey(User, on_delete=models.CASCADE)


    def __str__(self):
        return self.title