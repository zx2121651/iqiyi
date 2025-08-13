from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    UserRegistrationView,
    UserMeView,
    UserDetailView,
    FollowToggleView,
    FollowersListView,
    FollowingListView
)

urlpatterns = [
    # 用户认证相关
    path('auth/register/', UserRegistrationView.as_view(), name='user-register'),
    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # 用户信息相关
    path('users/me/', UserMeView.as_view(), name='user-me'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),

    # 关注功能相关
    path('users/<int:user_id>/follow/', FollowToggleView.as_view(), name='follow-toggle'),
    path('users/<int:user_id>/followers/', FollowersListView.as_view(), name='followers-list'),
    path('users/<int:user_id>/following/', FollowingListView.as_view(), name='following-list'),
]
