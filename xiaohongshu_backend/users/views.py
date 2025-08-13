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
