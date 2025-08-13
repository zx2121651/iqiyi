from rest_framework import generics, permissions, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.db.models import Q, Count
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer

User = get_user_model()

class ConversationListView(generics.ListAPIView):
    """
    获取当前用户的会话列表
    """
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # 预取参与者和最新的消息以优化性能
        return self.request.user.conversations.prefetch_related('participants', 'messages').all()


class MessageListCreateView(generics.ListCreateAPIView):
    """
    获取会话中的消息列表，或在会话中发送新消息
    """
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        只返回属于特定会话的消息，并确保当前用户是该会话的参与者。
        """
        conversation_id = self.kwargs['conversation_id']
        conversation = generics.get_object_or_404(
            Conversation.objects.prefetch_related('participants'),
            id=conversation_id
        )
        # 验证用户是否是会话的一部分
        if self.request.user not in conversation.participants.all():
            raise PermissionDenied("你无权访问此会话。")

        # 将获取的消息标记为已读（除了自己发送的）
        conversation.messages.exclude(sender=self.request.user).update(is_read=True)

        return conversation.messages.order_by('created_at')

    def perform_create(self, serializer):
        """
        发送消息时，自动设置发送者和会话。
        """
        conversation_id = self.kwargs['conversation_id']
        conversation = generics.get_object_or_404(Conversation, id=conversation_id)
        # 再次验证权限
        if self.request.user not in conversation.participants.all():
            raise PermissionDenied("你不能在此会话中发送消息。")

        serializer.save(sender=self.request.user, conversation=conversation)


class StartConversationView(generics.CreateAPIView):
    """
    与另一个用户开始一个新的会话（如果尚不存在），并发送第一条消息。
    """
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        recipient_id = self.kwargs['recipient_id']
        recipient = generics.get_object_or_404(User, id=recipient_id)
        sender = request.user

        if recipient == sender:
            return Response({"error": "你不能和自己开始会话。"}, status=status.HTTP_400_BAD_REQUEST)

        # 查找或创建会话
        conversation = None
        # 获取发送者参与的所有会话
        sender_conversations = Conversation.objects.filter(participants=sender).prefetch_related('participants')
        for conv in sender_conversations:
            # 检查参与者是否完全匹配
            if conv.participants.count() == 2 and recipient in conv.participants.all():
                conversation = conv
                break

        if not conversation:
            conversation = Conversation.objects.create()
            conversation.participants.add(sender, recipient)

        # 创建消息
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(sender=sender, conversation=conversation)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
