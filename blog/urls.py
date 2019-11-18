from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import (
	TokenObtainPairView,
	TokenRefreshView
)

from .views import *

router = routers.DefaultRouter()
router.register('users', UserViewSet)
router.register('posts', PostViewSet)

urlpatterns = [
	path('', api_root),
	path('', include(router.urls)),
	path('account/register/', RegistrationView.as_view(), name='account-register'),
	path('account/token/', TokenObtainPairView.as_view(), name='account-token'),
	path('account/refresh/', TokenRefreshView.as_view(), name='account-refresh')
]
