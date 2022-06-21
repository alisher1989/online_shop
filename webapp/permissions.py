from rest_framework import permissions
from webapp.models import Favorite


class CustomerAccessPermission(permissions.BasePermission):
    message = 'Доступ запрещен'

    def has_permission(self, request, view):
        try:
            obj = Favorite.objects.get(pk=view.kwargs['pk'])
            return request.user == obj.user
        except:
            return True
