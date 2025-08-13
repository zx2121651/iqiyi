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
    class Meta:
        model = User
        fields = ('id', 'username', 'nickname', 'avatar', 'bio', 'phone_number')
