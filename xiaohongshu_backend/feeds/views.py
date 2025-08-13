from rest_framework import generics, permissions
from django.db.models import Count, Prefetch

from xiaohongshu_backend.notes.models import Note
from xiaohongshu_backend.notes.serializers import NoteSerializer
from xiaohongshu_backend.interactions.models import Comment


class FollowingFeedView(generics.ListAPIView):
    """
    获取当前用户关注的人发布的笔记信息流
    """
    serializer_class = NoteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        返回当前用户关注的所有用户发布的笔记列表。
        """
        # 获取当前用户关注的所有用户的 ID 列表
        followed_users_ids = self.request.user.following.values_list('followed_id', flat=True)

        # 基于这个 ID 列表过滤笔记
        queryset = Note.objects.filter(author_id__in=followed_users_ids)

        # 复制 NoteViewSet 中的优化，以确保序列化器能高效工作
        optimized_queryset = queryset.annotate(
            likes_count=Count('likes', distinct=True),
            comments_count=Count('comments', distinct=True)
        ).prefetch_related(
            'images',
            'likes',
            'favorites'
        ).order_by('-created_at')

        return optimized_queryset


class ExploreFeedView(generics.ListAPIView):
    """
    获取“发现”信息流，包含系统中所有的笔记
    """
    serializer_class = NoteSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        """
        返回所有笔记的列表，并进行性能优化。
        """
        queryset = Note.objects.all()

        optimized_queryset = queryset.annotate(
            likes_count=Count('likes', distinct=True),
            comments_count=Count('comments', distinct=True)
        ).prefetch_related(
            'images',
            'likes',
            'favorites'
        ).order_by('-created_at')

        return optimized_queryset
