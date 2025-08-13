from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Conversation, Message
from xiaohongshu_backend.users.serializers import UserSerializer

User = get_user_model()

class MessageSerializer(serializers.ModelSerializer):
    """
    消息模型的序列化器
    """
    is_me = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = ['id', 'sender', 'text', 'created_at', 'is_read', 'is_me']
        read_only_fields = ['sender', 'created_at', 'is_read', 'is_me']

    def get_is_me(self, obj):
        """检查消息是否由当前请求用户发送"""
        return obj.sender == self.context['request'].user


class ConversationSerializer(serializers.ModelSerializer):
    """
    会话模型的序列化器
    """
    # 动态计算会话的名称（即对方的用户名）和头像
    other_participant = serializers.SerializerMethodField()
    last_message = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ['id', 'other_participant', 'last_message', 'updated_at']

    def get_other_participant(self, obj):
        """获取除当前用户外的另一个参与者信息"""
        current_user = self.context['request'].user
        other = obj.participants.exclude(id=current_user.id).first()
        if other:
            # 复用 UserSerializer 来序列化对方用户信息，但只取必要字段
            return {
                'id': other.id,
                'username': other.username,
                'nickname': other.nickname,
                'avatar': other.avatar.url if other.avatar else None
            }
        return None

    def get_last_message(self, obj):
        """获取会话的最后一条消息"""
        last_msg = obj.messages.order_by('-created_at').first()
        if last_msg:
            # 只返回文本和时间，保持列表简洁
            return {
                'text': last_msg.text,
                'created_at': last_msg.created_at,
                'is_read': last_msg.is_read
            }
        return None
