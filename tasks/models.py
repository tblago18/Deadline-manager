from django.db import models
from django.contrib.auth.models import User


class Task(models.Model):

	user = models.ForeignKey('auth.User', on_delete=models.CASCADE, null=True)
	title = models.CharField(max_length=200)
	complete = models.BooleanField(default=False)
	created = models.DateTimeField(auto_now_add=True)
	due_date = models.DateTimeField(null=True)
	notes = models.TextField(blank= True)


def __str__(self):
	return self.title
