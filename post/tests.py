from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from django.contrib.auth.models import User
from .models import Post


class PostTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.author = User.objects.create(
            username='UserTest',
        )
        self.post = Post.objects.create(
            title='Test Post',
            content='This is a test post.',
            author=self.author,
            release_date='2022-12-12',
            state='release'
        )

    def test_get_post(self):
        url = reverse('post-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
