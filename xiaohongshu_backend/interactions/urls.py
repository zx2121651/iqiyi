from django.urls import path
from .views import (
    CommentListCreateView,
    CommentDestroyView,
    LikeToggleView,
    FavoriteToggleView,
)

urlpatterns = [
    # 评论相关URL
    path('notes/<int:note_id>/comments/', CommentListCreateView.as_view(), name='comment-list-create'),
    path('comments/<int:pk>/', CommentDestroyView.as_view(), name='comment-destroy'),

    # 点赞和收藏相关URL
    path('notes/<int:note_id>/like/', LikeToggleView.as_view(), name='like-toggle'),
    path('notes/<int:note_id>/favorite/', FavoriteToggleView.as_view(), name='favorite-toggle'),
]
