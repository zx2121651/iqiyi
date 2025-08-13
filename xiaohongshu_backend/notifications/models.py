from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class Notification(models.Model):
    """
    通知模型
    """
    # 通知类型
    TYPE_LIKE = 'like'
    TYPE_COMMENT = 'comment'
    TYPE_FOLLOW = 'follow'
    TYPE_REPLY = 'reply'
    TYPE_CHOICES = [
        (TYPE_LIKE, '收到了赞'),
        (TYPE_COMMENT, '收到了评论'),
        (TYPE_FOLLOW, '收到了关注'),
        (TYPE_REPLY, '收到了回复'),
    ]

    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications',
        verbose_name="接收者"
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='sent_notifications',
        verbose_name="发送者"
    )
    verb = models.CharField(max_length=20, choices=TYPE_CHOICES, verbose_name="通知类型")

    # 通用外键，指向动作的直接对象，例如一个 Comment 或 Like 实例
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    action_object = GenericForeignKey('content_type', 'object_id')

    is_read = models.BooleanField(default=False, db_index=True, verbose_name="是否已读")
    created_at = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name="创建时间")

    class Meta:
        verbose_name = "通知"
        verbose_name_plural = verbose_name
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.sender} {self.verb} {self.recipient}"
