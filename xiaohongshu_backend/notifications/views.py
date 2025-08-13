from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Notification
from .serializers import NotificationSerializer

class NotificationListView(generics.ListAPIView):
    """
    获取当前用户的通知列表
    """
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        只返回当前用户的通知。
        可以通过查询参数 `?unread=true` 来只看未读通知。
        """
        user = self.request.user
        queryset = Notification.objects.filter(recipient=user)

        # 预取发送者和关联对象以优化性能
        queryset = queryset.select_related('sender').prefetch_related('action_object')

        unread_only = self.request.query_params.get('unread', 'false').lower() == 'true'
        if unread_only:
            queryset = queryset.filter(is_read=False)

        return queryset


class MarkAsReadView(APIView):
    """
    将单条或所有通知标记为已读
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk=None):
        """
        如果提供了 pk，则标记单条为已读。
        否则，标记所有为已读。
        """
        user = request.user

        if pk:
            # 标记单条
            try:
                notification = Notification.objects.get(pk=pk, recipient=user)
                notification.is_read = True
                notification.save()
                return Response({'status': 'notification marked as read'}, status=status.HTTP_200_OK)
            except Notification.DoesNotExist:
                return Response({'error': 'Notification not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            # 标记全部
            Notification.objects.filter(recipient=user, is_read=False).update(is_read=True)
            return Response({'status': 'all notifications marked as read'}, status=status.HTTP_200_OK)
