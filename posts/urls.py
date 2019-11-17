from django.urls import path, include
from rest_framework import routers

from .views import *

router = routers.DefaultRouter()
router.register('users', UserViewSet)

urlpatterns = [
	path('', api_root),
	path('', include(router.urls)),
	path('posts/', PostList.as_view(), name='post-list'),
	path('posts/<int:pk>/', PostDetail.as_view(), name='post-detail'),
]
