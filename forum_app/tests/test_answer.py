# from django.urls import reverse
# from rest_framework.test import APITestCase, APIClient
# from rest_framework import status
# from django.contrib.auth.models import User
# from rest_framework.authtoken.models import Token
# from forum_app.models import Answer, Question


# class AnswerTests(APITestCase):


#     def setUp(self):
#         """
#         Hiermit erstellen wir uns Testdaten für die Testdatenbank die automatisiert erstellt wird.
#         """
#         self.user = User.objects.create_user(
#             username='testuser', password='testpassword')
#         self.admin_user = User.objects.create_superuser(username='admin', password='admin')
#         self.question_1 = Question.objects.create(
#             title='Test Quotation', content='Test content', author=self.user, category='frontend')
#         self.question_2 = Question.objects.create(
#             title='Test Quotation Number 2', content='Test content 2', author=self.user, category='backend')
#         self.answer_1 = Answer.objects.create(content="Answer1", author=self.user, question=self.question_1)
#         self.answer_2 = Answer.objects.create(content="Answer2", author=self.user, question=self.question_1)
#         self.answer_3 = Answer.objects.create(content="Answer3", author=self.user, question=self.question_2)

#         self.token = Token.objects.create(user=self.user)
#         self.admin_token = Token.objects.create(user=self.admin_user)
#         self.client = APIClient()
#         self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)


#     def test_get_answer(self):
#         url = reverse('answer-list-create')
#         self.client.credentials()
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)


#     def test_get_answers_to_question_id(self):
#         url = reverse('answer-list-create')
#         response = self.client.get(url)

#         filter_answer_question = [answer for answer in response.data if answer['question'] == self.question_1.id]

#         self.assertEqual(len(filter_answer_question), 2)


#     def test_get_answer_detail_as_owner(self):
#         url = reverse('answer-detail', kwargs={'pk': self.answer_1.id})
#         response = self.client.get(url)

#         self.assertEqual(response.status_code, status.HTTP_200_OK)


#     def test_get_answer_detail_as_admin(self):
#         url = reverse('answer-detail', kwargs={'pk': self.answer_2.id})
#         response = self.client.get(url)

#         self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.admin_token.key)

#         self.assertEqual(response.status_code, status.HTTP_200_OK)


#     def test_create_answer_as_user(self):
#         url = reverse('answer-list-create')
#         data = {
#             'content':'Test Content',
#             'author': 1,
#             'question': 1
#         }
#         response = self.client.post(url, data, format='json')

#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)


#     def test_create_answer_unauthorized(self):
#         url = reverse('answer-list-create')
#         data = {
#             'content':'Test Content',
#             'author': 1,
#             'question': 1
#         }
#         self.client.credentials()
#         response = self.client.post(url, data, format='json')

#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


#     def test_create_answer_without_content(self):
#         url = reverse('answer-list-create')
#         data = {
#             'content':'',
#             'author': 1,
#             'question': 1
#         }
#         response = self.client.post(url, data, format='json')

#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


#     def test_edit_answer_as_owner(self):
#         url = reverse('answer-detail', kwargs={'pk': self.answer_1.id})
#         data = {
#             'content':'Test to Edit as Owner'
#         }
#         response = self.client.patch(url, data, format='json')

#         self.assertEqual(response.status_code, status.HTTP_200_OK)


#     def test_edit_answer_as_unauthorized(self):
#         url = reverse('answer-detail', kwargs={'pk': self.answer_1.id})
#         data = {
#             'content':'Test to Edit as Owner'
#         }
#         self.client.credentials()
#         response = self.client.patch(url, data, format='json')

#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


#     def test_delete_answer_as_owner(self):
#         url = reverse('answer-detail', kwargs={'pk': self.answer_2.id})
#         response = self.client.delete(url)

#         self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


#     def test_delete_answer_as_unauthorized(self):
#         url = reverse('answer-detail', kwargs={'pk': self.answer_2.id})
#         self.client.credentials()
#         response = self.client.delete(url)

#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)