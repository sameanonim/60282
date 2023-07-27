from rest_framework.permissions import BasePermission

class IsInModeratorGroup(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.groups.filter(name='moderators').exists())
    
class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        return obj.owner == request.user