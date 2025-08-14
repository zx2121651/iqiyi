from rest_framework import viewsets, permissions
from django.db.models import Count
from .models import Note
from .serializers import NoteSerializer
from .permissions import IsOwnerOrReadOnly
from .tasks import generate_thumbnail_task

class NoteViewSet(viewsets.ModelViewSet):
    """
    一个用于查看和编辑笔记的 ViewSet。
    """
    serializer_class = NoteSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_queryset(self):
        """
        重写 get_queryset 以添加注解和预取，优化性能。
        """
        return Note.objects.annotate(
            likes_count=Count('likes', distinct=True),
            comments_count=Count('comments', distinct=True)
        ).prefetch_related(
            'images', 'likes', 'favorites'
        )

    def perform_create(self, serializer):
        """
        在创建新笔记时，将作者设置为当前登录的用户。
        如果是视频笔记，则分发一个异步任务来为其生成缩略图。
        """
        note = serializer.save(author=self.request.user)
        if note.post_type == Note.POST_TYPE_VIDEO and note.video:
            # 调用Celery任务，.delay()使其在后台执行
            generate_thumbnail_task.delay(note.id)
