from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from .models import Conversation, Message

User = get_user_model()

class MessagingAPITests(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='password123')
        self.user2 = User.objects.create_user(username='user2', password='password456')
        self.user3 = User.objects.create_user(username='user3', password='password789')

    def test_start_conversation_and_send_message(self):
        """测试开始一个新会话并发送第一条消息"""
        self.client.force_authenticate(user=self.user1)
        url = reverse('start-conversation', kwargs={'recipient_id': self.user2.id})
        data = {'text': 'Hello, User2!'}

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertTrue(Conversation.objects.filter(participants=self.user1).filter(participants=self.user2).exists())
        self.assertEqual(Message.objects.count(), 1)
        self.assertEqual(Message.objects.first().sender, self.user1)

    def test_start_conversation_with_existing_does_not_create_new_convo(self):
        """测试与已存在会话的用户发消息不会创建新会话"""
        self.client.force_authenticate(user=self.user1)
        url = reverse('start-conversation', kwargs={'recipient_id': self.user2.id})

        # 第一次POST, 创建会话和第一条消息
        self.client.post(url, {'text': 'First message.'}, format='json')
        self.assertEqual(Conversation.objects.count(), 1)
        self.assertEqual(Message.objects.count(), 1)

        # 第二次POST, 应该只创建第二条消息
        self.client.post(url, {'text': 'Second message.'}, format='json')
        self.assertEqual(Conversation.objects.count(), 1)
        self.assertEqual(Message.objects.count(), 2)

    def test_list_conversations(self):
        """测试获取用户的会话列表"""
        # 设置初始状态: user1 和 user2 之间有会话
        convo = Conversation.objects.create()
        convo.participants.add(self.user1, self.user2)
        Message.objects.create(conversation=convo, sender=self.user1, text='Hello there')

        # 以user1身份请求会话列表
        self.client.force_authenticate(user=self.user1)
        url = reverse('conversation-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['other_participant']['username'], 'user2')
        self.assertEqual(response.data[0]['last_message']['text'], 'Hello there')

    def test_list_and_create_messages_in_conversation(self):
        """测试获取会话消息列表和在其中发送新消息"""
        # 设置初始状态: user1 和 user2 之间有会话和一条消息
        convo = Conversation.objects.create()
        convo.participants.add(self.user1, self.user2)
        Message.objects.create(conversation=convo, sender=self.user1, text='Initial message')

        url = reverse('message-list-create', kwargs={'conversation_id': convo.id})

        # user2 发送回复
        self.client.force_authenticate(user=self.user2)
        reply_data = {'text': 'Hi, User1!'}
        response = self.client.post(url, reply_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Message.objects.count(), 2)

        # user1 获取消息列表
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[1]['text'], 'Hi, User1!')

    def test_user_cannot_access_unrelated_conversation(self):
        """测试用户不能访问自己未参与的会话"""
        # 设置初始状态: user1 和 user2 之间有会话
        convo = Conversation.objects.create()
        convo.participants.add(self.user1, self.user2)
        url = reverse('message-list-create', kwargs={'conversation_id': convo.id})

        # user3 尝试访问
        self.client.force_authenticate(user=self.user3)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = self.client.post(url, {'text': 'Intruder!'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_messages_are_marked_as_read(self):
        """测试获取消息时，消息被标记为已读"""
        # 设置初始状态: user1 发送消息给 user2
        convo = Conversation.objects.create()
        convo.participants.add(self.user1, self.user2)
        message = Message.objects.create(conversation=convo, sender=self.user1, text='A message to be read.')
        self.assertFalse(message.is_read)

        # user2 获取该消息
        self.client.force_authenticate(user=self.user2)
        messages_url = reverse('message-list-create', kwargs={'conversation_id': convo.id})
        self.client.get(messages_url)

        # 再次检查消息状态
        message.refresh_from_db()
        self.assertTrue(message.is_read)
