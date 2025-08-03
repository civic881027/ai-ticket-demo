# tickets/permissions.py
from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsOwnerOrAdmin(BasePermission):
    """
    只允許工單建立者或管理員可修改，其他只能讀取
    """

    def has_object_permission(self, request, view, obj):
        # GET, HEAD, OPTIONS 等安全方法全部允許
        if request.method in SAFE_METHODS:
            return True

        # 編輯或刪除限擁有者或管理員
        return request.user.is_staff or obj.created_by == request.user

