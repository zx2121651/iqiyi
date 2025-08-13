from rest_framework import permissions

class IsOwner(permissions.BasePermission):
    """
    自定义权限，只允许对象的所有者操作它。
    """

    def has_object_permission(self, request, view, obj):
        # 写入权限只给对象的所有者。
        # 假设模型实例有一个 'author' 或 'user' 属性。
        if hasattr(obj, 'author'):
            return obj.author == request.user
        elif hasattr(obj, 'user'):
            return obj.user == request.user
        return False
