from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from rest_framework.authtoken.models import Token
from forum_app.models import Question, Like
from django.contrib.auth.models import User


class LikeTests(APITestCase):

    def setUp(self):
        """
        Hiermit erstellen wir uns Testdaten für die Testdatenbank die automatisiert erstellt wird.
        """
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')
        self.admin_user = User.objects.create_superuser(username='admin', password='admin')
        self.question_1 = Question.objects.create(
            title='Test Quotation', content='Test content', author=self.user, category='frontend')
        self.question_2 = Question.objects.create(
            title='Test Quotation Number 2', content='Test content 2', author=self.user, category='backend')
        self.like_1 = Like.objects.create(user=self.user, question=self.question_1)

        self.token = Token.objects.create(user=self.user)
        self.admin_token = Token.objects.create(user=self.admin_user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)


    def test_get_like(self):
        url = reverse('like-list')
        respone = self.client.get(url)
        self.assertEqual(respone.status_code, status.HTTP_200_OK)


    def test_create_like_as_user(self):
        url = reverse('like-list')
        data = {
            'user':self.user.id,
            'question':self.question_2.id
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    def test_create_like_as_unauthorized(self):
        url = reverse('like-list')
        data = {
            'user':self.user.id,
            'question':self.question_2.id
        }
        self.client.credentials()
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_check_dont_double_like_as_user(self):
        url = reverse('like-list')
        data = {
            'user':self.user.id,
            'question':self.question_1.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_delete_like_as_owner(self):
        url = reverse('like-detail', kwargs={'pk': self.like_1.id})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


    def test_delete_like_as_unauthorized(self):
        url = reverse('like-detail', kwargs={'pk': self.like_1.id})
        self.client.credentials()
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)