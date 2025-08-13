from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from xiaohongshu_backend.notes.models import Note

User = get_user_model()

class SearchAPITests(APITestCase):
    def setUp(self):
        # 创建用户
        self.user1 = User.objects.create_user(username='testuser1', password='password123', nickname='AlphaTester')
        self.user2 = User.objects.create_user(username='testuser2', password='password456', nickname='BetaUser')

        # 创建笔记
        self.note1 = Note.objects.create(author=self.user1, title='A Note About Django', content='Django is a Python framework.')
        self.note2 = Note.objects.create(author=self.user2, title='A Note About Testing', content='Testing is important in Python.')

        # 定义 URLs
        self.search_notes_url = reverse('search-notes')
        self.search_users_url = reverse('search-users')

    # --- 笔记搜索测试 ---
    def test_search_notes_by_title(self):
        """测试通过标题搜索笔记"""
        response = self.client.get(self.search_notes_url, {'q': 'Django'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], self.note1.id)

    def test_search_notes_by_content(self):
        """测试通过内容搜索笔记"""
        response = self.client.get(self.search_notes_url, {'q': 'framework'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], self.note1.id)

    def test_search_notes_multiple_results(self):
        """测试搜索返回多个结果"""
        response = self.client.get(self.search_notes_url, {'q': 'Python'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_search_notes_case_insensitive(self):
        """测试搜索不区分大小写"""
        response = self.client.get(self.search_notes_url, {'q': 'django'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_search_notes_no_results(self):
        """测试搜索没有结果时返回空列表"""
        response = self.client.get(self.search_notes_url, {'q': 'JavaScript'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_search_notes_no_query(self):
        """测试没有提供查询参数时返回空列表"""
        response = self.client.get(self.search_notes_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    # --- 用户搜索测试 ---
    def test_search_users_by_username(self):
        """测试通过用户名搜索用户"""
        response = self.client.get(self.search_users_url, {'q': 'testuser1'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], self.user1.id)

    def test_search_users_by_nickname(self):
        """测试通过昵称搜索用户"""
        response = self.client.get(self.search_users_url, {'q': 'Alpha'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], self.user1.id)

    def test_search_users_multiple_results(self):
        """测试用户搜索返回多个结果"""
        response = self.client.get(self.search_users_url, {'q': 'user'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
