from django.urls import path, include
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register('blog', views.PostDetail)

urlpatterns = [
	path('', include(router.urls)),
	path('users/', views.UserList.as_view()),
	path('users/<int:pk>', views.UserDetail.as_view())
]
