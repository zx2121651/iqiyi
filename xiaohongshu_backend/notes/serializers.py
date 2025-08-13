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
    video = serializers.FileField(write_only=True, required=False)

    class Meta:
        model = Note
        fields = [
            'id', 'author_username', 'title', 'content', 'post_type',
            'created_at', 'updated_at', 'images', 'video', 'video_thumbnail',
            'uploaded_images', 'likes_count', 'comments_count',
            'is_liked', 'is_favorited'
        ]
        read_only_fields = ['post_type', 'video_thumbnail']

    def validate(self, data):
        # This validation logic is for creation only.
        if self.instance is None:
            has_images = 'uploaded_images' in data and data['uploaded_images']
            has_video = 'video' in data and data['video']

            if not has_images and not has_video:
                raise serializers.ValidationError("创建新笔记时必须提供图片或视频。")

            if has_images and has_video:
                raise serializers.ValidationError("不能同时上传图片和视频。")

            if has_video:
                data['post_type'] = Note.POST_TYPE_VIDEO
            else:
                data['post_type'] = Note.POST_TYPE_IMAGE

        # For updates, if user uploads a new video or new images, we could add logic here
        # but for now we keep it simple and don't allow changing post type or media.

        return data

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
        重写 create 方法以处理图片或视频的上传
        """
        uploaded_images_data = validated_data.pop('uploaded_images', [])
        # video 数据已在 validated_data 中，随note实例一同创建

        note = Note.objects.create(**validated_data)

        if note.post_type == Note.POST_TYPE_IMAGE:
            for image_data in uploaded_images_data:
                NoteImage.objects.create(note=note, image=image_data)

        # 视频的缩略图生成将在 view 中处理

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
