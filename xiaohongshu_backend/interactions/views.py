from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import Comment, Like, Favorite
from .serializers import CommentSerializer
from .permissions import IsOwner
from xiaohongshu_backend.notes.models import Note


class CommentListCreateView(generics.ListCreateAPIView):
    """
    获取某篇笔记的评论列表，或为该笔记创建新评论。
    """
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        """
        只返回顶层评论（没有父评论的评论）。
        回复将通过序列化器中的 'replies' 字段嵌套显示。
        """
        note_id = self.kwargs['note_id']
        return Comment.objects.filter(note_id=note_id, parent=None)

    def perform_create(self, serializer):
        """
        创建评论时，自动设置作者和所属笔记。
        """
        note = get_object_or_404(Note, id=self.kwargs['note_id'])
        serializer.save(author=self.request.user, note=note)


class CommentDestroyView(generics.DestroyAPIView):
    """
    删除单条评论。
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]


class LikeToggleView(APIView):
    """
    点赞或取消点赞一篇笔记。
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, note_id):
        note = get_object_or_404(Note, id=note_id)
        like, created = Like.objects.get_or_create(user=request.user, note=note)

        if not created:
            # 如果 like 对象已存在，则表示是取消点赞，删除它
            like.delete()
            return Response({'status': 'unliked'}, status=status.HTTP_204_NO_CONTENT)

        # 如果是新创建的，表示点赞成功
        return Response({'status': 'liked'}, status=status.HTTP_201_CREATED)


class FavoriteToggleView(APIView):
    """
    收藏或取消收藏一篇笔记。
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, note_id):
        note = get_object_or_404(Note, id=note_id)
        favorite, created = Favorite.objects.get_or_create(user=request.user, note=note)

        if not created:
            # 如果 favorite 对象已存在，则表示是取消收藏，删除它
            favorite.delete()
            return Response({'status': 'unfavorited'}, status=status.HTTP_204_NO_CONTENT)

        # 如果是新创建的，表示收藏成功
        return Response({'status': 'favorited'}, status=status.HTTP_201_CREATED)
