from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from xiaohongshu_backend.notes.models import Note
from .models import Report

User = get_user_model()

class ModerationAPITests(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='password123')
        self.user2 = User.objects.create_user(username='user2', password='password456')
        self.note_by_user1 = Note.objects.create(author=self.user1, title='A Test Note', content='Content')

        self.report_url = reverse('report-create')

    def test_create_report_authenticated(self):
        """测试认证用户可以成功提交举报"""
        self.client.force_authenticate(user=self.user2)

        note_content_type = ContentType.objects.get_for_model(Note)
        data = {
            'content_type_model': f'notes.note',
            'object_id': self.note_by_user1.id,
            'reason': Report.REASON_SPAM,
            'details': 'This looks like spam.'
        }

        response = self.client.post(self.report_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Report.objects.count(), 1)

        report = Report.objects.first()
        self.assertEqual(report.reporter, self.user2)
        self.assertEqual(report.content_object, self.note_by_user1)
        self.assertEqual(report.reason, Report.REASON_SPAM)

    def test_create_report_unauthenticated(self):
        """测试未认证用户不能提交举报"""
        note_content_type = ContentType.objects.get_for_model(Note)
        data = {
            'content_type_model': f'notes.note',
            'object_id': self.note_by_user1.id,
            'reason': Report.REASON_SPAM,
        }
        response = self.client.post(self.report_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_report_nonexistent_content(self):
        """测试举报不存在的内容会失败"""
        self.client.force_authenticate(user=self.user2)
        data = {
            'content_type_model': 'notes.note',
            'object_id': 9999, # 不存在的ID
            'reason': Report.REASON_SPAM,
        }
        response = self.client.post(self.report_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_duplicate_report_fails(self):
        """测试用户不能重复举报相同内容"""
        self.client.force_authenticate(user=self.user2)
        note_content_type = ContentType.objects.get_for_model(Note)
        data = {
            'content_type_model': 'notes.note',
            'object_id': self.note_by_user1.id,
            'reason': Report.REASON_SPAM,
        }
        # 第一次举报
        self.client.post(self.report_url, data, format='json')
        self.assertEqual(Report.objects.count(), 1)

        # 第二次举报
        response = self.client.post(self.report_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Report.objects.count(), 1) # 确认数量没有增加
