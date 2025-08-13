from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """
    自定义用户模型
    """
    nickname = models.CharField(max_length=50, blank=True, null=True, verbose_name="昵称")
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name="头像")
    phone_number = models.CharField(max_length=15, unique=True, blank=True, null=True, verbose_name="手机号")
    bio = models.TextField(blank=True, null=True, verbose_name="个人简介")

    class Meta:
        verbose_name = "用户"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username
