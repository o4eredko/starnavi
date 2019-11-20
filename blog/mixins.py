from django.contrib.contenttypes.models import ContentType
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.models import User

from .models import Like
from .serializers import UserSerializer, PostSerializer


class LikesMixin:
	@action(detail=True, methods=['POST'], permission_classes=[IsAuthenticated])
	def like(self, request, pk=None):
		obj = self.get_object()
		obj_type = ContentType.objects.get_for_model(obj)
		Like.objects.get_or_create(content_type=obj_type, object_id=obj.id, user=request.user)

		serializer = PostSerializer(obj, context={'request': request})
		return Response(serializer.data)

	@action(detail=True, methods=['POST'], permission_classes=[IsAuthenticated])
	def unlike(self, request, pk=None):
		obj = self.get_object()
		obj_type = ContentType.objects.get_for_model(obj)
		Like.objects.filter(content_type=obj_type, object_id=obj.id, user=request.user).delete()

		serializer = PostSerializer(obj, context={'request': request})
		return Response(serializer.data)

	@action(detail=True, methods=['GET'])
	def fans(self, request, pk=None):
		obj = self.get_object()
		obj_type = ContentType.objects.get_for_model(obj)
		fans = User.objects.filter(likes__content_type=obj_type, likes__object_id=obj.id)

		serializer = UserSerializer(fans, many=True, context={'request': request})
		return Response(serializer.data)
