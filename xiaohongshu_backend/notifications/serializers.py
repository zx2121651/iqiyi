from rest_framework import serializers
from .models import Notification
from django.contrib.auth import get_user_model
from xiaohongshu_backend.notes.models import Note
from xiaohongshu_backend.interactions.models import Comment
from xiaohongshu_backend.users.serializers import UserSerializer

User = get_user_model()

class GenericRelatedField(serializers.Field):
    """
    一个自定义字段，用于序列化不同类型的关联对象。
    """
    def to_representation(self, value):
        if isinstance(value, User):
            return UserSerializer(value, context=self.context).data
        if isinstance(value, Note):
            # 使用一个简化的Note序列化器，避免数据过于庞大
            return {'id': value.id, 'title': value.title}
        if isinstance(value, Comment):
            return {'id': value.id, 'content': value.content}
        return str(value)

class NotificationSerializer(serializers.ModelSerializer):
    """
    通知序列化器
    """
    sender = UserSerializer(read_only=True)
    action_object = GenericRelatedField(read_only=True)

    class Meta:
        model = Notification
        fields = [
            'id', 'sender', 'verb', 'action_object',
            'is_read', 'created_at'
        ]
