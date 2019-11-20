from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

registration_url = reverse('account-register')
login_url = reverse('account-token')
refresh_url = reverse('account-refresh')


class RegistrationTestCase(APITestCase):
	user = {
		'username': 'test_username',
		'email': 'test_email@gmail.com',
		'password': 'SecretPassword123',
		'password2': 'SecretPassword123'
	}

	def test_registration(self):
		response = self.client.post(registration_url, self.user)
		self.assertEquals(response.status_code, status.HTTP_201_CREATED)

	def test_registration_error_invalid_password(self):
		data = dict(self.user)
		data['password'] = data['password2'] = '123'
		response = self.client.post(registration_url, data)
		self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

		# passwords not equal
		data['password'] = self.user['password']
		response = self.client.post(registration_url, data)
		self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

	def test_registration_error_data_exists(self):
		data = dict(self.user)
		self.client.post(registration_url, data)

		# check if username exists
		response = self.client.post(registration_url, data)
		self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

		# check if email exists
		data['username'] = 'test_username2'
		response = self.client.post(registration_url, data)
		self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

	def test_registration_error_data_missing(self):
		data = dict(self.user)
		data.pop('username')
		response = self.client.post(registration_url, data)
		self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

		data = dict(self.user)
		data.pop('email')
		response = self.client.post(registration_url, data)
		self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)


class TokenLoginTestCase(APITestCase):
	def setUp(self):
		self.user = {
			'username': 'test_username',
			'email': 'test_email@gmail.com',
			'password': 'SecretPassword123',
			'password2': 'SecretPassword123'
		}
		self.client.post(registration_url, self.user)

	def test_login_error_wrong_data(self):
		login_data = {'username': self.user['username'], 'password': '123'}
		response = self.client.post(login_url, login_data)
		self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)

		login_data = {'username': 'admin', 'password': 'admin'}
		response = self.client.post(login_url, login_data)
		self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)

	def test_login(self):
		login_data = {'username': self.user['username'], 'password': self.user['password']}
		response = self.client.post(login_url, login_data)
		self.assertEquals(response.status_code, status.HTTP_200_OK)


class TokenRefreshTestCase(APITestCase):
	def setUp(self):
		user = {
			'username': 'test_username',
			'email': 'test_email@gmail.com',
			'password': 'SecretPassword123',
			'password2': 'SecretPassword123'
		}
		self.client.post(registration_url, user)

		login_data = {'username': user['username'], 'password': user['password']}
		response = self.client.post(login_url, login_data)
		self.access_token = response.data['access']
		self.refresh_token = response.data['refresh']

	def test_refresh_error_wrong_token(self):
		refresh_data = {'refresh': '123'}
		response = self.client.post(refresh_url, refresh_data)
		self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)

	def test_refresh(self):
		refresh_data = {'refresh': self.refresh_token}
		response = self.client.post(refresh_url, refresh_data)
		self.access_token = response.data['access']
		self.assertEquals(response.status_code, status.HTTP_200_OK)


class UserViewSetTestCase(APITestCase):
	def setUp(self):
		user = {
			'username': 'test_username',
			'email': 'test_email@gmail.com',
			'password': 'SecretPassword123',
			'password2': 'SecretPassword123'
		}
		self.client.post(registration_url, user)
		user['username'] = 'test_username2'
		user['email'] = 'test_email2@gmail.com'
		self.client.post(registration_url, user)

	def test_user_list(self):
		response = self.client.get(reverse('user-list'))
		self.assertEquals(response.status_code, status.HTTP_200_OK)

	def test_user_detail(self):
		response = self.client.get(reverse('user-list'))
		self.assertEquals(response.status_code, status.HTTP_200_OK)
		last_user = response.data[-1]
		response = self.client.get(last_user['url'])
		self.assertEquals(response.status_code, status.HTTP_200_OK)


class PostViewSetTestCase(APITestCase):
	post_list_url = reverse('post-list')

	def setUp(self):
		user = {
			'username': 'test_username',
			'email': 'test_email@gmail.com',
			'password': 'SecretPassword123',
			'password2': 'SecretPassword123'
		}
		self.client.post(registration_url, user)
		login_data = {'username': user['username'], 'password': user['password']}
		response = self.client.post(login_url, login_data)
		self.access_token = response.data['access']

		user['username'] = 'test_username_2'
		user['email'] = 'test_email2@gmail.com'
		self.client.post(registration_url, user)
		login_data = {'username': user['username'], 'password': user['password']}
		response = self.client.post(login_url, login_data)
		self.second_user_access_token = response.data['access']

	def create_post(self):
		self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
		response = self.client.post(self.post_list_url, {'title': 'Title', 'content': 'Content'})
		return response

	def test_post_create_unauthorized(self):
		post_data = {'title': 'Title', 'content': 'Post content'}
		response = self.client.post(self.post_list_url, post_data)
		self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)

	def test_post_create(self):
		self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
		post_data = {'title': 'Title', 'content': 'Post content'}
		response = self.client.post(self.post_list_url, post_data)
		self.assertEquals(response.status_code, status.HTTP_201_CREATED)

	def test_post_create_error_missing_data(self):
		self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
		response = self.client.post(self.post_list_url, {'title': 'Title'})
		self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
		response = self.client.post(self.post_list_url, {'content': 'Content'})
		self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

	def test_post_detail(self):
		self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
		self.client.post(self.post_list_url, {'title': 'Title', 'content': 'Content'})
		self.client.post(self.post_list_url, {'title': 'Title', 'content': 'Content'})
		self.client.post(self.post_list_url, {'title': 'Title', 'content': 'Content'})

		response = self.client.get(self.post_list_url)
		self.assertEquals(response.status_code, status.HTTP_200_OK)
		self.assertEquals(response.data['count'], 3)

		last_post = response.data['results'][-1]
		response = self.client.get(last_post['url'])
		self.assertEquals(response.status_code, status.HTTP_200_OK)

	def test_post_like(self):
		post_response = self.create_post()
		self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.second_user_access_token)
		response = self.client.post(reverse('post-like', kwargs={'pk': post_response.data['id']}))
		self.assertEquals(response.status_code, status.HTTP_200_OK)
		self.assertTrue(response.data['is_fan'])

	def test_post_unlike(self):
		post_response = self.create_post()
		response = self.client.post(reverse('post-like', kwargs={'pk': post_response.data['id']}))
		self.assertTrue(response.data['is_fan'])

		response = self.client.post(reverse('post-unlike', kwargs={'pk': post_response.data['id']}))
		self.assertFalse(response.data['is_fan'])

	def test_post_multiple_likes(self):
		# post_response = self.create_post()
		# response = self.client
		pass
