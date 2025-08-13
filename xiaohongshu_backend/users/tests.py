from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

User = get_user_model()

class UserAuthAPITests(APITestCase):
    """
    用户认证流程的API测试
    """

    def setUp(self):
        """
        初始化测试数据
        """
        self.register_url = reverse('user-register')
        self.login_url = reverse('token_obtain_pair')
        self.me_url = reverse('user-me')

        # 用户注册数据
        self.user_data = {
            'username': 'testuser',
            'password': 'testpassword123',
            'phone_number': '13100001111',
            'nickname': '测试用户'
        }
        # 另一个用户的数据，用于测试唯一性
        self.user_data2 = {
            'username': 'testuser2',
            'password': 'testpassword456',
        }

    def test_user_registration_success(self):
        """
        测试用户成功注册
        """
        response = self.client.post(self.register_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'testuser')
        self.assertNotIn('password', response.data) # 确认响应中不包含密码

    def test_user_registration_duplicate_username(self):
        """
        测试使用重复用户名注册失败
        """
        # 先创建一个用户
        self.client.post(self.register_url, self.user_data, format='json')
        # 尝试用相同的用户名创建另一个用户
        duplicate_data = self.user_data.copy()
        duplicate_data['phone_number'] = '13200002222' # 换个手机号
        response = self.client.post(self.register_url, duplicate_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_login_and_get_me(self):
        """
        测试用户登录以及使用token获取个人信息
        """
        # 1. 先注册用户
        self.client.post(self.register_url, self.user_data, format='json')

        # 2. 登录获取 token
        login_data = {
            'username': self.user_data['username'],
            'password': self.user_data['password']
        }
        response = self.client.post(self.login_url, login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

        access_token = response.data['access']

        # 3. 使用 access token 访问受保护的 'me' 接口
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        response = self.client.get(self.me_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], self.user_data['username'])
        self.assertEqual(response.data['phone_number'], self.user_data['phone_number'])

    def test_get_me_unauthenticated(self):
        """
        测试未认证用户访问 'me' 接口失败
        """
        response = self.client.get(self.me_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
