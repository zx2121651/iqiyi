from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import get_user_model
from .serializers import UserRegistrationSerializer, UserSerializer

User = get_user_model()

class UserRegistrationView(generics.CreateAPIView):
    """
    用户注册视图
    允许任何人访问 (AllowAny)
    """
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]


class UserMeView(generics.RetrieveAPIView):
    """
    获取当前登录用户信息的视图
    需要认证 (IsAuthenticated)
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        """
        重写 get_object 方法，直接返回当前登录的用户
        """
        return self.request.user


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from xiaohongshu_backend.interactions.models import Follow


class FollowToggleView(APIView):
    """
    关注或取消关注一个用户
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        followed_user = get_object_or_404(User, id=user_id)
        follower_user = request.user

        if follower_user == followed_user:
            return Response({"error": "用户不能关注自己"}, status=status.HTTP_400_BAD_REQUEST)

        follow, created = Follow.objects.get_or_create(
            follower=follower_user,
            followed=followed_user
        )

        if not created:
            follow.delete()
            return Response({'status': 'unfollowed'}, status=status.HTTP_204_NO_CONTENT)

        return Response({'status': 'followed'}, status=status.HTTP_201_CREATED)


class FollowersListView(generics.ListAPIView):
    """
    获取一个用户的粉丝列表
    """
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        # 查找所有关注了 `user_id` 的关注关系
        # 然后通过 `follower` 字段反向获取这些用户
        return User.objects.filter(following__followed_id=user_id)


class FollowingListView(generics.ListAPIView):
    """
    获取一个用户关注的人的列表
    """
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        # 查找所有 `user_id` 是关注者的关注关系
        # 然后通过 `followed` 字段获取这些被关注的用户
        return User.objects.filter(followers__follower_id=user_id)


from .serializers import PublicUserProfileSerializer
from django.db.models import Prefetch
from xiaohongshu_backend.notes.models import Note

class UserDetailView(generics.RetrieveAPIView):
    """
    获取用户公开主页的视图
    """
    serializer_class = PublicUserProfileSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        """
        重写 get_queryset 以进行深度预取，优化性能。
        """
        # 预取用户发布的笔记，并且对每个笔记，再预取其图片、点赞和收藏
        notes_prefetch = Prefetch(
            'notes',
            queryset=Note.objects.prefetch_related('images', 'likes', 'favorites')
        )
        # 预取用户的关注者和被关注者关系
        return User.objects.prefetch_related(
            notes_prefetch, 'followers', 'following'
        )
