from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import UserRegistrationView, UserMeView

urlpatterns = [
    # 用户认证相关
    path('auth/register/', UserRegistrationView.as_view(), name='user-register'),
    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # 用户信息相关
    path('users/me/', UserMeView.as_view(), name='user-me'),
]
