from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models


class Like(models.Model):
	user = models.ForeignKey('auth.User', related_name='likes', on_delete=models.CASCADE)
	content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
	object_id = models.PositiveIntegerField()
	content_object = GenericForeignKey('content_type', 'object_id')


class Post(models.Model):
	title = models.CharField(max_length=140)
	content = models.TextField()
	created = models.DateTimeField(auto_now_add=True)
	author = models.ForeignKey('auth.User', related_name='posts', on_delete=models.CASCADE)
	likes = GenericRelation(Like)

	def __str__(self):
		return self.title

	@property
	def total_likes(self):
		return self.likes.count()
