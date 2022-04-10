from rest_framework import permissions


class CreatePostPermissions(permissions.BasePermission):

    def has_permission(self, request, view):
        user = request.user
        user_groups = user.groups.values_list('name',flat = True)
        if 'BlogStaff'  in user_groups:
            return True
        return False
