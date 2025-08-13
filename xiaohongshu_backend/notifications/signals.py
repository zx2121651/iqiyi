from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from xiaohongshu_backend.interactions.models import Like, Comment, Follow
from .models import Notification

User = get_user_model()

@receiver(post_save, sender=Like)
def notify_on_like(sender, instance, created, **kwargs):
    """
    当有点赞时，创建通知
    """
    if created:
        # 避免给自己点赞时发送通知
        if instance.user != instance.note.author:
            Notification.objects.create(
                recipient=instance.note.author,
                sender=instance.user,
                verb=Notification.TYPE_LIKE,
                action_object=instance.note
            )

@receiver(post_save, sender=Comment)
def notify_on_comment(sender, instance, created, **kwargs):
    """
    当有评论或回复时，创建通知
    """
    if created:
        # 如果是回复
        if instance.parent:
            # 避免回复自己时发送通知
            if instance.author != instance.parent.author:
                Notification.objects.create(
                    recipient=instance.parent.author,
                    sender=instance.author,
                    verb=Notification.TYPE_REPLY,
                    action_object=instance
                )
        # 如果是顶级评论
        else:
            # 避免评论自己的笔记时发送通知
            if instance.author != instance.note.author:
                 Notification.objects.create(
                    recipient=instance.note.author,
                    sender=instance.author,
                    verb=Notification.TYPE_COMMENT,
                    action_object=instance
                )

@receiver(post_save, sender=Follow)
def notify_on_follow(sender, instance, created, **kwargs):
    """
    当有新的关注时，创建通知
    """
    if created:
        Notification.objects.create(
            recipient=instance.followed,
            sender=instance.follower,
            verb=Notification.TYPE_FOLLOW,
            action_object=instance.follower
        )
