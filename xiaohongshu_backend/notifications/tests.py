from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from xiaohongshu_backend.notes.models import Note
from xiaohongshu_backend.interactions.models import Like, Comment, Follow
from .models import Notification

User = get_user_model()

class NotificationAPITests(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='password123')
        self.user2 = User.objects.create_user(username='user2', password='password456')
        self.note_by_user1 = Note.objects.create(author=self.user1, title='Note by User1', content='Content')

    # --- 信号触发测试 ---
    def test_like_creates_notification(self):
        """测试点赞创建通知"""
        Like.objects.create(user=self.user2, note=self.note_by_user1)
        self.assertEqual(Notification.objects.count(), 1)
        notification = Notification.objects.first()
        self.assertEqual(notification.recipient, self.user1)
        self.assertEqual(notification.sender, self.user2)
        self.assertEqual(notification.verb, Notification.TYPE_LIKE)

    def test_comment_creates_notification(self):
        """测试评论创建通知"""
        Comment.objects.create(author=self.user2, note=self.note_by_user1, content="A comment")
        self.assertEqual(Notification.objects.count(), 1)
        notification = Notification.objects.first()
        self.assertEqual(notification.recipient, self.user1)
        self.assertEqual(notification.sender, self.user2)
        self.assertEqual(notification.verb, Notification.TYPE_COMMENT)

    def test_follow_creates_notification(self):
        """测试关注创建通知"""
        Follow.objects.create(follower=self.user2, followed=self.user1)
        self.assertEqual(Notification.objects.count(), 1)
        notification = Notification.objects.first()
        self.assertEqual(notification.recipient, self.user1)
        self.assertEqual(notification.sender, self.user2)
        self.assertEqual(notification.verb, Notification.TYPE_FOLLOW)

    def test_no_notification_for_self_action(self):
        """测试用户自己的行为不会创建通知"""
        Like.objects.create(user=self.user1, note=self.note_by_user1)
        self.assertEqual(Notification.objects.count(), 0)

    # --- API 端点测试 ---
    def test_list_notifications(self):
        """测试获取通知列表"""
        # 创建一个通知
        Follow.objects.create(follower=self.user2, followed=self.user1)

        self.client.force_authenticate(user=self.user1)
        url = reverse('notification-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['verb'], Notification.TYPE_FOLLOW)

    def test_mark_one_as_read(self):
        """测试将单条通知标记为已读"""
        follow_notification = Follow.objects.create(follower=self.user2, followed=self.user1)
        notification = Notification.objects.get(recipient=self.user1)
        self.assertFalse(notification.is_read)

        self.client.force_authenticate(user=self.user1)
        url = reverse('notification-mark-one-read', kwargs={'pk': notification.id})
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        notification.refresh_from_db()
        self.assertTrue(notification.is_read)

    def test_mark_all_as_read(self):
        """测试将所有通知标记为已读"""
        Follow.objects.create(follower=self.user2, followed=self.user1)
        Like.objects.create(user=self.user2, note=self.note_by_user1)
        self.assertEqual(Notification.objects.filter(recipient=self.user1, is_read=False).count(), 2)

        self.client.force_authenticate(user=self.user1)
        url = reverse('notification-mark-all-read')
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Notification.objects.filter(recipient=self.user1, is_read=False).count(), 0)

    def test_user_cannot_access_others_notifications(self):
        """测试用户不能访问或修改他人的通知"""
        # user2 关注 user1, user1 收到通知
        Follow.objects.create(follower=self.user2, followed=self.user1)
        notification_for_user1 = Notification.objects.get(recipient=self.user1)

        # user2 尝试获取通知列表，应该为空
        self.client.force_authenticate(user=self.user2)
        list_url = reverse('notification-list')
        response = self.client.get(list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

        # user2 尝试标记 user1 的通知为已读，应该失败
        mark_url = reverse('notification-mark-one-read', kwargs={'pk': notification_for_user1.id})
        response = self.client.post(mark_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
