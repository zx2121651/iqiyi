from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class Report(models.Model):
    """
    内容举报模型
    """
    # 举报理由选项
    REASON_SPAM = 'spam'
    REASON_INAPPROPRIATE = 'inappropriate'
    REASON_HATE_SPEECH = 'hate_speech'
    REASON_OTHER = 'other'
    REASON_CHOICES = [
        (REASON_SPAM, '垃圾广告'),
        (REASON_INAPPROPRIATE, '不当内容'),
        (REASON_HATE_SPEECH, '仇恨言论'),
        (REASON_OTHER, '其他'),
    ]

    # 举报处理状态
    STATUS_PENDING = 'pending'
    STATUS_REVIEWED_ACTION_TAKEN = 'action_taken'
    STATUS_REVIEWED_NO_ACTION = 'no_action'
    STATUS_CHOICES = [
        (STATUS_PENDING, '待处理'),
        (STATUS_REVIEWED_ACTION_TAKEN, '已处理'),
        (STATUS_REVIEWED_NO_ACTION, '已忽略'),
    ]

    reporter = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reports_made',
        verbose_name="举报人"
    )

    # 指向被举报内容的通用外键 (可以是笔记、评论等)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, verbose_name="被举报内容类型")
    object_id = models.PositiveIntegerField(verbose_name="被举报对象ID")
    content_object = GenericForeignKey('content_type', 'object_id')

    reason = models.CharField(max_length=20, choices=REASON_CHOICES, verbose_name="举报理由")
    details = models.TextField(blank=True, null=True, verbose_name="详细信息")

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_PENDING,
        db_index=True,
        verbose_name="处理状态"
    )

    created_at = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name="举报时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")


    class Meta:
        verbose_name = "举报"
        verbose_name_plural = verbose_name
        ordering = ['-created_at']
        # 确保一个用户对同一内容只能举报一次
        unique_together = ('reporter', 'content_type', 'object_id')

    def __str__(self):
        return f"Report by {self.reporter.username} on object {self.object_id}"
