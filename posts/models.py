from django.db import models
from django.contrib.contenttypes.fields import GenericRelation

from likes.models import Like


class Post(models.Model):
	title = models.CharField(max_length=140)
	content = models.TextField()
	creation_date = models.DateTimeField(auto_now_add=True)
	likes = GenericRelation(Like)

	def __str__(self):
		return self.title

	@property
	def total_likes(self):
		return self.likes.count()
