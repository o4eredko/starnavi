from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from . import services
from .serializers import UserSerializer


class LikedMixin:
	@action(detail=True, methods=['POST'], permission_classes=[IsAuthenticated])
	def like(self, request, pk=None):
		obj = self.get_object()
		serializer = self.get_serializer(obj)
		services.add_like(obj, request.user)
		return Response(serializer.data)

	@action(detail=True, methods=['POST'], permission_classes=[IsAuthenticated])
	def unlike(self, request, pk=None):
		obj = self.get_object()
		serializer = self.get_serializer(obj)
		services.remove_like(obj, request.user)
		return Response(serializer.data)

	@action(detail=True, methods=['GET'])
	def fans(self, request, pk=None):
		obj = self.get_object()
		fans = services.get_fans(obj)
		serializer = UserSerializer(fans, many=True, context={'request': request})
		return Response(serializer.data)
