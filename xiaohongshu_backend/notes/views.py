from rest_framework import viewsets, permissions
from .models import Note
from .serializers import NoteSerializer
from .permissions import IsOwnerOrReadOnly

class NoteViewSet(viewsets.ModelViewSet):
    """
    一个用于查看和编辑笔记的 ViewSet。
    """
    queryset = Note.objects.all().prefetch_related('images')
    serializer_class = NoteSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        """
        在创建新笔记时，将作者设置为当前登录的用户。
        """
        serializer.save(author=self.request.user)
