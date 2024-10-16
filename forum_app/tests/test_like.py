from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status


class LikeTests(APITestCase):

    def test_get_like(self):
        url = reverse('like-list')
        respone = self.client.get(url)
        self.assertEqual(respone.status_code, status.HTTP_200_OK)