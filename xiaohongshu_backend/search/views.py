from rest_framework import generics, permissions
from django.db.models import Q, Count
from xiaohongshu_backend.notes.models import Note
from xiaohongshu_backend.notes.serializers import NoteSerializer

class NoteSearchView(generics.ListAPIView):
    """
    根据关键词搜索笔记
    """
    serializer_class = NoteSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        """
        根据查询参数 'q' 过滤笔记的标题和内容。
        """
        query = self.request.query_params.get('q', None)
        if query:
            # 使用 Q 对象进行 OR 查询，i_contains 表示不区分大小写的包含查询
            search_queryset = Note.objects.filter(
                Q(title__icontains=query) | Q(content__icontains=query)
            )

            # 复制其他视图中的查询优化
            optimized_queryset = search_queryset.annotate(
                likes_count=Count('likes', distinct=True),
                comments_count=Count('comments', distinct=True)
            ).prefetch_related(
                'images', 'likes', 'favorites'
            ).order_by('-created_at')

            return optimized_queryset

        # 如果没有提供查询参数，返回空列表
        return Note.objects.none()


from django.contrib.auth import get_user_model
from xiaohongshu_backend.users.serializers import UserSerializer

User = get_user_model()

class UserSearchView(generics.ListAPIView):
    """
    根据关键词搜索用户
    """
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        """
        根据查询参数 'q' 过滤用户的用户名和昵称。
        """
        query = self.request.query_params.get('q', None)
        if query:
            return User.objects.filter(
                Q(username__icontains=query) | Q(nickname__icontains=query)
            )

        return User.objects.none()
