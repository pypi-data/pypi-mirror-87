from rest_framework.permissions import BasePermission


class IsSuperuser(BasePermission):
    """
    Allows access only to supper users.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)


class RbacPermission(BasePermission):
    """
    基于角色的认证系统的权限校验类
    """

    def has_permission(self, request, view):

        print('request.user.is_supperuser',
              request._request.method.lower())
        print('request.path_info', request.path_info)
        if request.user and request.user.is_superuser:
            return True


class ObjectPermission(BasePermission):
    '''
    密码管理对象级权限控制
    '''

    def has_object_permission(self, request, view, obj):
        print('request.user.id', request.user.id)
        if request.user and request.user.is_superuser:
            return True
        elif request.user.id == obj.user_id:
            return True
