from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from xiaohongshu_backend.notes.models import Note
from xiaohongshu_backend.interactions.models import Follow

User = get_user_model()

class FeedsAPITests(APITestCase):
    def setUp(self):
        # 创建用户
        self.user1 = User.objects.create_user(username='user1', password='password123')
        self.user2 = User.objects.create_user(username='user2', password='password456')
        self.user3 = User.objects.create_user(username='user3', password='password789')

        # user1 关注 user2
        Follow.objects.create(follower=self.user1, followed=self.user2)

        # 创建笔记
        self.note1_by_user1 = Note.objects.create(author=self.user1, title='Note by User1', content='Content 1')
        self.note2_by_user2 = Note.objects.create(author=self.user2, title='Note by User2', content='Content 2')
        self.note3_by_user3 = Note.objects.create(author=self.user3, title='Note by User3', content='Content 3')

        # 定义 URLs
        self.following_feed_url = reverse('feed-following')
        self.explore_feed_url = reverse('feed-explore')

    def test_following_feed_authenticated(self):
        """
        测试登录用户获取“关注”信息流
        """
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(self.following_feed_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # 响应中应该只有一篇笔记
        self.assertEqual(len(response.data), 1)

        # 确认这篇笔记是 user2 发布的
        response_note_ids = {note['id'] for note in response.data}
        self.assertIn(self.note2_by_user2.id, response_note_ids)

        # 确认不包含 user1 和 user3 的笔记
        self.assertNotIn(self.note1_by_user1.id, response_note_ids)
        self.assertNotIn(self.note3_by_user3.id, response_note_ids)

    def test_following_feed_unauthenticated(self):
        """
        测试未登录用户不能访问“关注”信息流
        """
        response = self.client.get(self.following_feed_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_explore_feed(self):
        """
        测试任何人都可以访问“发现”信息流
        """
        response = self.client.get(self.explore_feed_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # 应该包含所有三篇笔记
        self.assertEqual(len(response.data), 3)

        # 验证返回的笔记ID
        response_note_ids = {note['id'] for note in response.data}
        self.assertIn(self.note1_by_user1.id, response_note_ids)
        self.assertIn(self.note2_by_user2.id, response_note_ids)
        self.assertIn(self.note3_by_user3.id, response_note_ids)

        # 验证排序是否正确（按创建时间倒序）
        first_note_id_in_response = response.data[0]['id']
        self.assertEqual(first_note_id_in_response, self.note3_by_user3.id)
