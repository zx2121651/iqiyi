from rest_framework import serializers
from .models import Note, NoteImage
from django.contrib.auth import get_user_model

User = get_user_model()

class NoteImageSerializer(serializers.ModelSerializer):
    """
    笔记图片序列化器
    """
    class Meta:
        model = NoteImage
        fields = ['id', 'image', 'uploaded_at']


class NoteSerializer(serializers.ModelSerializer):
    """
    笔记序列化器
    """
    author_username = serializers.ReadOnlyField(source='author.username')
    images = NoteImageSerializer(many=True, read_only=True)

    # 动态计算字段
    likes_count = serializers.IntegerField(read_only=True)
    comments_count = serializers.IntegerField(read_only=True)
    is_liked = serializers.SerializerMethodField()
    is_favorited = serializers.SerializerMethodField()

    uploaded_images = serializers.ListField(
        child=serializers.ImageField(allow_empty_file=False, use_url=False),
        write_only=True,
        required=False
    )

    class Meta:
        model = Note
        fields = [
            'id', 'author_username', 'title', 'content',
            'created_at', 'updated_at', 'images', 'uploaded_images',
            'likes_count', 'comments_count', 'is_liked', 'is_favorited'
        ]

    def get_is_liked(self, obj):
        user = self.context['request'].user
        if user.is_anonymous:
            return False
        return obj.likes.filter(user=user).exists()

    def get_is_favorited(self, obj):
        user = self.context['request'].user
        if user.is_anonymous:
            return False
        return obj.favorites.filter(user=user).exists()

    def create(self, validated_data):
        """
        重写 create 方法以处理图片上传
        """
        # 弹出非模型字段
        uploaded_images_data = validated_data.pop('uploaded_images', [])

        # 首先创建 Note 实例
        note = Note.objects.create(**validated_data)

        # 遍历上传的图片并为每个图片创建 NoteImage 实例
        for image_data in uploaded_images_data:
            NoteImage.objects.create(note=note, image=image_data)

        return note

    def update(self, instance, validated_data):
        """
        重写 update 方法以处理图片上传 (如果需要)
        注意：这里的实现很简单，只是添加新图片，并不会删除旧图片。
        一个完整的实现可能需要更复杂的逻辑来处理图片的增、删、改。
        """
        uploaded_images_data = validated_data.pop('uploaded_images', [])

        # 更新 Note 模型的字段
        instance.title = validated_data.get('title', instance.title)
        instance.content = validated_data.get('content', instance.content)
        instance.save()

        # 创建新的 NoteImage 实例
        for image_data in uploaded_images_data:
            NoteImage.objects.create(note=instance, image=image_data)

        return instance
