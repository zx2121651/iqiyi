from django.db import models
from django.conf import settings

class Conversation(models.Model):
    """
    会话模型，代表两个或多个用户之间的对话。
    """
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='conversations',
        verbose_name="参与者"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        verbose_name = "会话"
        verbose_name_plural = verbose_name
        ordering = ['-updated_at']

    def __str__(self):
        return f"Conversation between {', '.join([user.username for user in self.participants.all()])}"


class Message(models.Model):
    """
    消息模型，代表会话中的单条消息。
    """
    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name='messages',
        verbose_name="所属会话"
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='sent_messages',
        verbose_name="发送者"
    )
    text = models.TextField(verbose_name="消息内容")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    is_read = models.BooleanField(default=False, verbose_name="是否已读")

    class Meta:
        verbose_name = "消息"
        verbose_name_plural = verbose_name
        ordering = ['created_at']

    def __str__(self):
        return f"Message from {self.sender.username} at {self.created_at}"
