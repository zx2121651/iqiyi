from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from xiaohongshu_backend.notes.models import Note
from .models import Comment, Like, Favorite

User = get_user_model()


class InteractionsAPITests(APITestCase):
    def setUp(self):
        # 创建用户
        self.user1 = User.objects.create_user(username='user1', password='password123')
        self.user2 = User.objects.create_user(username='user2', password='password456')

        # 创建笔记
        self.note = Note.objects.create(author=self.user1, title='Test Note', content='Test Content')

        # 定义 URLs
        self.comments_url = reverse('comment-list-create', kwargs={'note_id': self.note.id})
        self.like_url = reverse('like-toggle', kwargs={'note_id': self.note.id})
        self.favorite_url = reverse('favorite-toggle', kwargs={'note_id': self.note.id})

    # --- 评论测试 ---
    def test_create_comment_authenticated(self):
        """测试登录用户可以发表评论"""
        self.client.force_authenticate(user=self.user2)
        data = {'content': 'This is a comment.'}
        response = self.client.post(self.comments_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(Comment.objects.first().author, self.user2)

    def test_create_comment_unauthenticated(self):
        """测试未登录用户不能发表评论"""
        data = {'content': 'This comment should not be created.'}
        response = self.client.post(self.comments_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_comments(self):
        """测试可以获取某篇笔记的评论列表"""
        # user2 发表一条评论
        Comment.objects.create(author=self.user2, note=self.note, content='A test comment.')
        response = self.client.get(self.comments_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['content'], 'A test comment.')

    def test_delete_own_comment(self):
        """测试用户可以删除自己的评论"""
        comment = Comment.objects.create(author=self.user2, note=self.note, content='I will be deleted.')
        self.client.force_authenticate(user=self.user2)
        delete_url = reverse('comment-destroy', kwargs={'pk': comment.id})
        response = self.client.delete(delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Comment.objects.count(), 0)

    def test_delete_other_user_comment_forbidden(self):
        """测试用户不能删除他人的评论"""
        comment = Comment.objects.create(author=self.user2, note=self.note, content='Cannot delete this.')
        self.client.force_authenticate(user=self.user1) # Note author, not comment author
        delete_url = reverse('comment-destroy', kwargs={'pk': comment.id})
        response = self.client.delete(delete_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # --- 点赞测试 ---
    def test_like_and_unlike_note(self):
        """测试点赞和取消点赞的切换功能"""
        self.client.force_authenticate(user=self.user2)

        # 第一次请求：点赞
        response = self.client.post(self.like_url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.note.likes.count(), 1)
        self.assertTrue(Like.objects.filter(user=self.user2, note=self.note).exists())

        # 第二次请求：取消点赞
        response = self.client.post(self.like_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(self.note.likes.count(), 0)

    def test_like_unauthenticated(self):
        """测试未登录用户不能点赞"""
        response = self.client.post(self.like_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # --- 收藏测试 ---
    def test_favorite_and_unfavorite_note(self):
        """测试收藏和取消收藏的切换功能"""
        self.client.force_authenticate(user=self.user2)

        # 第一次请求：收藏
        response = self.client.post(self.favorite_url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.note.favorites.count(), 1)
        self.assertTrue(Favorite.objects.filter(user=self.user2, note=self.note).exists())

        # 第二次请求：取消收藏
        response = self.client.post(self.favorite_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(self.note.favorites.count(), 0)

    # --- 序列化器动态字段测试 ---
    def test_serializer_dynamic_fields(self):
        """测试 Note 序列化器中动态字段的正确性"""
        # user2 点赞并收藏
        self.client.force_authenticate(user=self.user2)
        self.client.post(self.like_url)
        self.client.post(self.favorite_url)

        # user1 发表一条评论
        Comment.objects.create(author=self.user1, note=self.note, content='A comment.')

        # 以 user2 的身份获取笔记详情
        note_detail_url = reverse('note-detail', kwargs={'pk': self.note.id})
        response = self.client.get(note_detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['likes_count'], 1)
        self.assertEqual(response.data['comments_count'], 1)
        self.assertTrue(response.data['is_liked'])
        self.assertTrue(response.data['is_favorited'])

        # 以 user1 的身份获取笔记详情
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(note_detail_url)
        self.assertFalse(response.data['is_liked']) # user1 没有点赞
        self.assertFalse(response.data['is_favorited']) # user1 没有收藏
