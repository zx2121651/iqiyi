import tempfile
from PIL import Image
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from .models import Note

User = get_user_model()

def get_temporary_image():
    """
    创建一个临时的图片文件用于测试上传
    """
    temp_file = tempfile.NamedTemporaryFile(suffix='.jpg', delete=False)
    image = Image.new('RGB', (10, 10), 'red')
    image.save(temp_file, 'jpeg')
    temp_file.seek(0)
    return temp_file


class NoteAPITests(APITestCase):
    """
    笔记功能API的测试
    """
    def setUp(self):
        # 创建两个用户
        self.user1 = User.objects.create_user(username='user1', password='password123')
        self.user2 = User.objects.create_user(username='user2', password='password456')

        # 创建一个笔记实例，作者是 user1
        self.note = Note.objects.create(author=self.user1, title='Note by User1', content='Content by User1')

        # 定义URL
        self.list_create_url = reverse('note-list')
        self.detail_url = reverse('note-detail', kwargs={'pk': self.note.pk})

    def test_list_notes_unauthenticated(self):
        """
        测试未登录用户可以获取笔记列表
        """
        response = self.client.get(self.list_create_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_note_unauthenticated(self):
        """
        测试未登录用户可以获取单个笔记
        """
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.note.title)

    def test_create_note_authenticated(self):
        """
        测试登录用户可以创建笔记
        """
        self.client.force_authenticate(user=self.user2)
        data = {'title': 'New Note by User2', 'content': 'Some new content.'}
        response = self.client.post(self.list_create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Note.objects.count(), 2)
        new_note = Note.objects.get(id=response.data['id'])
        self.assertEqual(new_note.author, self.user2)

    def test_create_note_with_image(self):
        """
        测试创建笔记时上传图片
        """
        self.client.force_authenticate(user=self.user1)
        image_file = get_temporary_image()
        data = {
            'title': 'Note with image',
            'content': 'This note has an image.',
            'uploaded_images': [image_file]
        }
        # 注意：文件上传需要使用 'multipart' 格式
        response = self.client.post(self.list_create_url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        new_note = Note.objects.get(id=response.data['id'])
        self.assertEqual(new_note.images.count(), 1)
        # 清理临时文件
        image_file.close()

    def test_create_note_unauthenticated(self):
        """
        测试未登录用户不能创建笔记
        """
        data = {'title': 'Unauthorized Note', 'content': 'This should fail.'}
        response = self.client.post(self.list_create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_note_by_owner(self):
        """
        测试笔记作者可以更新自己的笔记
        """
        self.client.force_authenticate(user=self.user1)
        data = {'title': 'Updated Title'}
        response = self.client.patch(self.detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.note.refresh_from_db()
        self.assertEqual(self.note.title, 'Updated Title')

    def test_update_note_by_non_owner(self):
        """
        测试非作者不能更新他人的笔记
        """
        self.client.force_authenticate(user=self.user2) # 使用 user2 登录
        data = {'title': 'Attempted Update by User2'}
        response = self.client.patch(self.detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_note_by_owner(self):
        """
        测试笔记作者可以删除自己的笔记
        """
        self.client.force_authenticate(user=self.user1)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Note.objects.count(), 0)

    def test_delete_note_by_non_owner(self):
        """
        测试非作者不能删除他人的笔记
        """
        self.client.force_authenticate(user=self.user2)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Note.objects.count(), 1)
