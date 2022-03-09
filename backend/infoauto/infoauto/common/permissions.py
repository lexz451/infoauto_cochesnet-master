# -*- coding: utf-8 -*-


from rest_framework.permissions import IsAdminUser as BaseIsAdminUser


class IsAdminUser(BaseIsAdminUser):
    def has_permission(self, request, view):
        return super().has_permission(request, view) or (request.user and request.user.is_superuser)
