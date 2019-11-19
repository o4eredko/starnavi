from django.contrib.auth.models import User
from rest_framework import viewsets, generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.reverse import reverse
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from .models import Post
from .permissions import IsOwnerOrReadOnly
from .serializers import PostSerializer, UserSerializer, RegistrationSerializer
from .mixins import LikesMixin


@api_view(['GET'])
def api_root(request, format=None):
	return Response({
		'users': reverse('user-list', request=request, format=format),
		'posts': reverse('post-list', request=request, format=format),
		'registration': reverse('account-register', request=request, format=format),
		'token-login': reverse('account-token', request=request, format=format),
		'token-refresh': reverse('account-refresh', request=request, format=format),
	})


class PostViewSet(LikesMixin, viewsets.ModelViewSet):
	queryset = Post.objects.all()
	serializer_class = PostSerializer
	permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
	pagination_class = PageNumberPagination
	pagination_class.page_size = 10

	def perform_create(self, serializer):
		serializer.save(author=self.request.user)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
	queryset = User.objects.all()
	serializer_class = UserSerializer


class RegistrationView(generics.CreateAPIView):
	queryset = User.objects.all()
	serializer_class = RegistrationSerializer

	def perform_create(self, serializer):
		data = {}
		if serializer.is_valid():
			user = serializer.save()
			data['response'] = 'successfully registered new user.'
			data['email'] = user.email
			data['username'] = user.username
		else:
			data = serializer.errors
		return Response(data)
