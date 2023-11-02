from rest_framework.permissions import SAFE_METHODS, BasePermission


class HasObjectPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        if request.user == obj.author:
            return True
        return False
