from rest_framework import serializers
from .models import Comment

class ReplySerializer(serializers.ModelSerializer):
    """
    用于嵌套显示的回复序列化器（二级评论）
    """
    author_username = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Comment
        fields = ['id', 'author_username', 'content', 'created_at']


class CommentSerializer(serializers.ModelSerializer):
    """
    主评论序列化器
    """
    author_username = serializers.ReadOnlyField(source='author.username')
    # 使用 ReplySerializer 来显示回复，避免无限嵌套
    replies = ReplySerializer(many=True, read_only=True)

    class Meta:
        model = Comment
        fields = [
            'id', 'author_username', 'content', 'created_at',
            'parent', 'replies'
        ]
        # parent 字段只在写入时需要，读取时我们通过嵌套的 replies 显示
        extra_kwargs = {
            'parent': {'write_only': True, 'required': False},
        }
