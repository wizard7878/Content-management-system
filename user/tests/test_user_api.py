import email
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from django.urls import reverse

USER_SIGNUP_URL = reverse("user:signup")
USER_SIGNIN_URL = reverse("user:signin")
USER_PROFILE_URL = reverse("user:profile")
USER_RESET_PASSWORD_URL = reverse('user:reset-password')

class PublicUserApiTests(TestCase):
    """
    User Api tests 
    """
    def setUp(self):
        self.client = APIClient()

    def test_user_signup_api(self):
        """
        Test signup user with payload data 
        """
        payload = {
            'email': 'test@email.ir',
            'username': 'testname',
            'bio': 'your bio',
            'password': 'Qwert123@',
            'confirm_password':'Qwert123@'
        }

        res = self.client.post(USER_SIGNUP_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data['username'], 'testname')

    def test_empty_password_signup_api(self):
        "test signup api without fill up password"

        payload = {
            'email' : 'test@email.com',
            'password' : '',
            'confirm_password': ''
        }

        res = self.client.post(USER_SIGNUP_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_bad_password_signup_api(self):
        "test signup api with bad password"

        payload = {
            'email' : 'test@email.com',
            'password' : 'ps',
            'confirm_password': 'ps'
        }

        res = self.client.post(USER_SIGNUP_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_signup_invalid_password(self):
        "test signin api with payload data"

        payload = {
            'email' : 'test3@email.com',
            'password' : 'qwert3434'
        }

        res = self.client.post(USER_SIGNUP_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


    def test_user_signin_api(self):
        "test signin api with payload data"

        payload = {
            'email' : 'test3@email.com',
            'password' : 'ASfge345'
        }

        user = get_user_model().objects.create_user(**payload)

        res = self.client.post(USER_SIGNIN_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('access', res.data)

    def test_invalid_user_signin_api(self):
        "test signin api with invalid data that is not exist"

        payload = {
            'email' : 'test3@email.com',
            'password' : '98787'
        }


        res = self.client.post(USER_SIGNIN_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertNotIn('access', res.data)

    def test_unseccessfull_user_signin_api(self):
        "Test signin api with invalid password"

        payload = {
            'email' : 'test3@email.com',
            'password' : ''
        }

        res = self.client.post(USER_SIGNIN_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('access', res.data)

    def test_retrieve_user_profile_unauthorized(self):
        """
        Test retrieve user profile data without sign in
        """
        res = self.client.get(USER_PROFILE_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_reset_password_unauthorized(self):
        """
        Test change password when you are not authenticated
        """

        payload = {
            'old_password': 'Testpassword123@',
            'new_password': 'Testpassword345@',
            'confirm_new_password': 'Testpassword345@'
        }

        res = self.client.put(USER_RESET_PASSWORD_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)



class PrivateUserApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(email = 'example@email.com',password = 'test132456')
        self.client.force_authenticate(self.user)

    def test_retrieve_user_profile(self):
        """
        Test retrieve user profile data
        """
        res = self.client.get(USER_PROFILE_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['email'] , 'example@email.com')

    def test_update_user_profile(self):
        """
        Test updating user profile datas
        """
        payload = {
            'email': 'example@gmail.com',
            'username': 'UsernameTest',
            'bio': 'your bio',
        }

        res = self.client.put(USER_PROFILE_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['email'], 'example@gmail.com')
        self.assertEqual('UsernameTest', res.data['username'])

    def test_invalid_update_user_profile(self):
        """
        Test updating user profile with invalid data
        """
        payload = {
            'username': 'UsernameTest',
        }

        res = self.client.put(USER_PROFILE_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('username', res.data)
    
    def test_patch_user_profile(self):
        """
        Test patch user profile datas
        """

        payload = {
            'username' : 'TestUsername'
        }

        res = self.client.patch(USER_PROFILE_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['email'], 'example@email.com')
        self.assertEqual('TestUsername', res.data['username'])

    def test_update_reset_password(self):
        """
        Test reset password api 
        """
        payload = {
            'old_password': 'test132456',
            'new_password': 'Testpassword345@',
            'confirm_new_password': 'Testpassword345@'
        }

        res = self.client.put(USER_RESET_PASSWORD_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_update_reset_password_invalid(self):
        """
        Test reset password with invalid old password
        """

        payload = {
            'old_password': 'test1324',
            'new_password': 'Testpassword345@',
            'confirm_new_password': 'Testpassword345@'
        }

        res = self.client.put(USER_RESET_PASSWORD_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


    def test_update_reset_password_invalid_form(self):
        """
        Test reset password with invalid form of password
        """

        payload = {
            'old_password': 'test1324',
            'new_password': 'Testpa',
            'confirm_new_password': 'Testpa'
        }

        res = self.client.put(USER_RESET_PASSWORD_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


