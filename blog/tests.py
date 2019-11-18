from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

registration_url = reverse('account-register')
login_url = reverse('account-token')
refresh_url = reverse('account-refresh')


class RegistrationTestCase(APITestCase):
	data = {
		'username': 'test_username',
		'email': 'test_email@gmail.com',
		'password': 'SecretPassword123',
		'password2': 'SecretPassword123'
	}

	def test_registration_valid(self):
		response = self.client.post(registration_url, self.data)
		self.assertEquals(response.status_code, status.HTTP_201_CREATED)

	def test_registration_invalid_passwords(self):
		data = dict(self.data)
		data['password'] = data['password2'] = '123'
		response = self.client.post(registration_url, data)
		self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

		# passwords not equal
		data['password'] = self.data['password']
		response = self.client.post(registration_url, data)
		self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

	def test_registration_data_exists(self):
		data = dict(self.data)
		self.client.post(registration_url, data)

		# check if username exists
		response = self.client.post(registration_url, data)
		self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

		# check if email exists
		data['username'] = 'test_username2'
		response = self.client.post(registration_url, data)
		self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

	def test_registration_data_missing(self):
		data = dict(self.data)
		data.pop('username')
		response = self.client.post(registration_url, data)
		self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

		data = dict(self.data)
		data.pop('email')
		response = self.client.post(registration_url, data)
		self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)


class TokenLoginTestCase(APITestCase):
	data = {
		'username': 'test_username',
		'email': 'test_email@gmail.com',
		'password': 'SecretPassword123',
		'password2': 'SecretPassword123'
	}

	def setUp(self):
		self.client.post(registration_url, self.data)

	def test_login_invalid(self):
		login_data = {'username': self.data['username'], 'password': '123'}
		response = self.client.post(login_url, login_data)
		self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)

	def test_login_valid(self):
		login_data = {'username': self.data['username'], 'password': self.data['password']}
		response = self.client.post(login_url, login_data)
		self.assertEquals(response.status_code, status.HTTP_200_OK)


class TokenRefreshTestCase(APITestCase):
	data = {
		'username': 'test_username',
		'email': 'test_email@gmail.com',
		'password': 'SecretPassword123',
		'password2': 'SecretPassword123'
	}

	def setUp(self):
		self.client.post(registration_url, self.data)
		login_data = {'username': self.data['username'], 'password': self.data['password']}
		response = self.client.post(login_url, login_data)
		self.access_token = response.data['access']
		self.refresh_token = response.data['refresh']

	def test_token_refresh_invalid(self):
		refresh_data = {'refresh': '123'}
		response = self.client.post(refresh_url, refresh_data)
		self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)

	def test_token_refresh_valid(self):
		refresh_data = {'refresh': self.refresh_token}
		response = self.client.post(refresh_url, refresh_data)
		self.access_token = response.data['access']
		self.assertEquals(response.status_code, status.HTTP_200_OK)
