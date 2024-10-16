from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth.models import User
from forum_app.models import Question
from forum_app.api.serializers import QuestionSerializer
from rest_framework.authtoken.models import Token


class QuestionTests(APITestCase):

    def setUp(self):
        """
        Hiermit erstellen wir uns Testdaten für die Testdatenbank die automatisiert erstellt wird.
        """
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')
        self.admin_user = User.objects.create_superuser(username='admin', password='admin')
        self.question = Question.objects.create(
            title='Test Quotation', content='Test content', author=self.user, category='frontend')
        # Möglichkeit 1 der Authorization
        # self.client = APIClient()
        # self.client.login(username='testuser', password='testpassword')

        # Möglichkeit 2 der Authorization
        self.token = Token.objects.create(user=self.user)
        self.admin_token = Token.objects.create(user=self.admin_user)
        # print(f"Token created:", self.token.key)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        
        

        # print(f"setUp User authenticated:", self.client.credentials())

    # def test_list_post_question_authorized(self):
    #     url = reverse('question-list')
    #     data = {
    #         'title': 'Question1',
    #         'content': 'Content1',
    #         'author': self.user.id,
    #         'category': 'frontend'
    #     }
    #     response = self.client.post(url, data, format='json')

    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    def test_list_post_question_authorized_without_title(self):
        url = reverse('question-list')
        data = {
            'content': 'Content1',
            'author': self.user.id,
            'category': 'frontend'
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    # def test_list_post_question_unauthorized(self):
    #     url = reverse('question-list')
    #     data = {
    #         'title': 'Question1',
    #         'content': 'Content1',
    #         'author': self.user.id,
    #         'category': 'frontend'
    #     }
    #     self.client.credentials()
    #     response = self.client.post(url, data, format='json')

    #     self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # def test_detail_question(self):
    #     url = reverse('question-detail', kwargs={'pk': self.question.id})
    #     response = self.client.get(url)
    #     expected_data = QuestionSerializer(self.question).data

    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(response.data, expected_data)
    #     self.assertDictEqual(response.data, expected_data)
    #     self.assertJSONEqual(response.content, expected_data)
    #     self.assertContains(response, 'title')

    # def test_question_list(self):
    #     url = reverse('question-list')
    #     response = self.client.get(url)

    #     self.assertEqual(response.status_code, status.HTTP_200_OK)

    # def test_edit_question_as_owner(self):

    #     url = reverse('question-detail', kwargs={'pk': self.question.id})
    #     print('URL', url)
    #     print(f"User authenticated:", self.client.credentials())
    #     print(f"Token being used:", self.token.key)
        
    #     data = {
    #         'title': 'Question1',
    #         'content': 'ContentEdit'
    #     }

    #     response = self.client.patch(url, data=data, format='json')
    #     print('Response status code:', response.status_code)
    #     print('Response data', response.data)

    #     self.assertEqual(response.status_code, status.HTTP_200_OK)


    # def test_edit_question_as_unauthorized(self):

    #     url = reverse('question-detail', kwargs={'pk': self.question.id})
    #     data = {
    #         'title': 'Question1',
    #         'content': 'ContentEdit'
    #     }
    #     self.client.credentials()
    #     response = self.client.patch(url, data=data, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


    # def test_delete_question_as_admin(self):
    #     url = reverse('question-detail', kwargs={'pk': self.question.id})
        
    #     self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.admin_token.key)

    #     response = self.client.delete(url)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_delete_question_as_admin(self):
        url = reverse('question-detail', kwargs={'pk': self.question.id})
        
        self.client.credentials()

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)