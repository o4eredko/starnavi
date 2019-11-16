from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
	def has_object_permission(self, request, view, obj):
		# Read permissions are allowed to any request,
		# so we'll always allow GET, HEAD or OPTIONS requests.
		if request.method in permissions.SAFE_METHODS:
			return True

		# Write permissions are only allowed to the owner of the snippet.
		return obj.author == request.user


class AllowPostAnyReadAuthenticatedUser(permissions.BasePermission):
	def has_permission(self, request, view):
		# Allow anyone to register
		if request.method == "POST":
			return True
		# Must be authenticated to view
		else:
			return request.user and is_authenticated(request.user)

	def has_object_permission(self, request, view, obj):
		# Any view method requires you to be the user
		return obj.id == request.user.id or request.user.is_superuser
