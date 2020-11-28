from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import APIException


class CustomForbidden(APIException):
    status_code = status.HTTP_404_NOT_FOUND


class IsOrder(permissions.BasePermission):

    def has_permission(self, request, view):
       return True

    def has_object_permission(self, request, view, obj):
        if obj.user == request.user:
            return True
        else:
            raise CustomForbidden


class IsAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.is_staff==True:
            return True

