from django.db import models
from django.conf import settings
from xiaohongshu_backend.notes.models import Note

class Comment(models.Model):
    """
    评论模型
    """
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name="作者"
    )
    note = models.ForeignKey(
        Note,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name="所属笔记"
    )
    content = models.TextField(verbose_name="评论内容")
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='replies',
        verbose_name="父评论"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    class Meta:
        verbose_name = "评论"
        verbose_name_plural = verbose_name
        ordering = ['created_at']

    def __str__(self):
        return f"Comment by {self.author.username} on {self.note.title}"


class Like(models.Model):
    """
    点赞模型
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='likes',
        verbose_name="用户"
    )
    note = models.ForeignKey(
        Note,
        on_delete=models.CASCADE,
        related_name='likes',
        verbose_name="笔记"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="点赞时间")

    class Meta:
        verbose_name = "点赞"
        verbose_name_plural = verbose_name
        # 联合唯一约束，确保一个用户只能对一篇笔记点赞一次
        unique_together = ('user', 'note')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} likes {self.note.title}"


class Favorite(models.Model):
    """
    收藏模型
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name="用户"
    )
    note = models.ForeignKey(
        Note,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name="笔记"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="收藏时间")

    class Meta:
        verbose_name = "收藏"
        verbose_name_plural = verbose_name
        # 联合唯一约束，确保一个用户只能收藏一篇笔记一次
        unique_together = ('user', 'note')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} favorited {self.note.title}"


class Follow(models.Model):
    """
    关注关系模型
    """
    # 关注者
    follower = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='following', # 我关注的人
        verbose_name="关注者"
    )
    # 被关注者
    followed = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='followers', # 我的粉丝
        verbose_name="被关注者"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="关注时间")

    class Meta:
        verbose_name = "关注"
        verbose_name_plural = verbose_name
        unique_together = ('follower', 'followed')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.follower.username} follows {self.followed.username}"
