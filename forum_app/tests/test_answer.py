from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status


class AnswerTests(APITestCase):

    def test_get_answer(self):
        """
        Die URL kann auch Hard im Code stehen. Macht jedoch eventuelle Änderungen an URL usw. problematisch.
        """
        url = reverse('answer-list-create')
        # url = 'http://127.0.0.1:8000/api/forum/answers/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)