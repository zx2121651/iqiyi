from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    用户注册序列化器
    """
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ('username', 'password', 'phone_number', 'nickname')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            phone_number=validated_data.get('phone_number'),
            nickname=validated_data.get('nickname')
        )
        return user

class UserSerializer(serializers.ModelSerializer):
    """
    用户基本信息序列化器
    """
    followers_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()
    is_following = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id', 'username', 'nickname', 'avatar', 'bio', 'phone_number',
            'followers_count', 'following_count', 'is_following'
        )

    def get_followers_count(self, obj):
        return obj.followers.count()

    def get_following_count(self, obj):
        return obj.following.count()

    def get_is_following(self, obj):
        requesting_user = self.context['request'].user
        if requesting_user.is_anonymous:
            return False
        # 检查请求用户是否是 obj 的粉丝 (即请求用户是否在 obj.followers 关系中作为 'follower')
        return obj.followers.filter(follower=requesting_user).exists()


from xiaohongshu_backend.notes.serializers import NoteSerializer

class PublicUserProfileSerializer(UserSerializer):
    """
    用户公开主页的序列化器，包含用户发布的笔记列表
    """
    # 'notes' 是在 User 模型中通过 related_name 定义的反向关系
    notes = NoteSerializer(many=True, read_only=True)

    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + ('notes',)
