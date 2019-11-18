from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase


class RegistrationTestCase(APITestCase):
	registration_url = reverse('account-register')
	data = {
		'username': 'test_username',
		'email': 'test_email@gmail.com',
		'password': 'SecretPassword123',
		'password2': 'SecretPassword123'
	}

	def test_registration_valid(self):
		response = self.client.post(self.registration_url, self.data)
		self.assertEquals(response.status_code, status.HTTP_201_CREATED)

	def test_registration_invalid_passwords(self):
		data = dict(self.data)
		data['password'] = data['password2'] = '123'
		response = self.client.post(self.registration_url, data)
		self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

		# passwords not equal
		data['password'] = self.data['password']
		response = self.client.post(self.registration_url, data)
		self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

	def test_registration_data_exists(self):
		data = dict(self.data)
		self.client.post(self.registration_url, data)

		# check if username exists
		response = self.client.post(self.registration_url, data)
		self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

		# check if email exists
		data['username'] = 'test_username2'
		response = self.client.post(self.registration_url, data)
		self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

	def test_registration_data_missing(self):
		data = dict(self.data)
		data.pop('username')
		response = self.client.post(self.registration_url, data)
		self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

		data = dict(self.data)
		data.pop('email')
		response = self.client.post(self.registration_url, data)
		self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
