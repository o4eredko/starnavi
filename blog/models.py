from django.db import models


class Post(models.Model):
	title = models.CharField(max_length=255)
	content = models.TextField()
	creation_date = models.DateTimeField(auto_now_add=True)
	author = models.ForeignKey('auth.User', related_name='posts', on_delete=models.CASCADE)

	def __str__(self):
		return self.title
