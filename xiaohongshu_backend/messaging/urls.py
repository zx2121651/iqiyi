from django.urls import path
from .views import (
    ConversationListView,
    MessageListCreateView,
    StartConversationView,
)

urlpatterns = [
    # 获取会话列表
    path('conversations/', ConversationListView.as_view(), name='conversation-list'),

    # 获取/发送特定会话中的消息
    path('conversations/<int:conversation_id>/messages/', MessageListCreateView.as_view(), name='message-list-create'),

    # 与指定用户开始会话并发送第一条消息
    path('users/<int:recipient_id>/messages/', StartConversationView.as_view(), name='start-conversation'),
]
