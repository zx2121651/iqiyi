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


from xiaohongshu_backend.interactions.models import Follow
from xiaohongshu_backend.notes.models import Note

class UserProfileAndFollowAPITests(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='password123')
        self.user2 = User.objects.create_user(username='user2', password='password456')
        Note.objects.create(author=self.user1, title='Note from User1', content='Content.')

    def test_follow_and_unfollow_user(self):
        """测试关注和取关用户"""
        self.client.force_authenticate(user=self.user2)
        follow_url = reverse('follow-toggle', kwargs={'user_id': self.user1.id})

        # 关注
        response = self.client.post(follow_url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Follow.objects.filter(follower=self.user2, followed=self.user1).exists())

        # 取关
        response = self.client.post(follow_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Follow.objects.filter(follower=self.user2, followed=self.user1).exists())

    def test_follow_self_not_allowed(self):
        """测试用户不能关注自己"""
        self.client.force_authenticate(user=self.user1)
        follow_url = reverse('follow-toggle', kwargs={'user_id': self.user1.id})
        response = self.client.post(follow_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_followers_and_following_list(self):
        """测试获取粉丝和关注列表"""
        Follow.objects.create(follower=self.user2, followed=self.user1)

        # 获取 user1 的粉丝列表 (应包含 user2)
        followers_url = reverse('followers-list', kwargs={'user_id': self.user1.id})
        response = self.client.get(followers_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['username'], self.user2.username)

        # 获取 user2 的关注列表 (应包含 user1)
        following_url = reverse('following-list', kwargs={'user_id': self.user2.id})
        response = self.client.get(following_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['username'], self.user1.username)

    def test_get_user_profile(self):
        """测试获取用户公开主页"""
        # user2 关注 user1
        Follow.objects.create(follower=self.user2, followed=self.user1)

        # 以 user2 的身份访问 user1 的主页
        self.client.force_authenticate(user=self.user2)
        profile_url = reverse('user-detail', kwargs={'pk': self.user1.id})
        response = self.client.get(profile_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], self.user1.username)
        self.assertEqual(response.data['followers_count'], 1)
        self.assertEqual(response.data['following_count'], 0)
        self.assertTrue(response.data['is_following'])
        self.assertEqual(len(response.data['notes']), 1)
        self.assertEqual(response.data['notes'][0]['title'], 'Note from User1')
