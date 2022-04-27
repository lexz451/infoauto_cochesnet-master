from django.conf import settings
from rest_framework.permissions import IsAuthenticated


class IsAllowedToken(IsAuthenticated):
    def has_permission(self, request, view):
        response = super().has_permission(request, view)
        if response:
            allowed_token = request.user.auth_token.key in getattr(settings, 'ALLOWED_TOKENS', [])
            return allowed_token or request.user.is_admin
        else:
            return response
