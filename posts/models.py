from django.contrib.auth.models import User
from django.db import models


class Post(models.Model):
	title = models.CharField(max_length=140)
	content = models.TextField()
	created = models.DateTimeField(auto_now_add=True)
	author = models.ForeignKey('auth.User', related_name='posts', on_delete=models.CASCADE)

	def __str__(self):
		return self.title
