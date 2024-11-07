import time

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from bitpin.posts.models import Post
from bitpin.posts.tasks import refresh_materialized_view

User = get_user_model()


class PostListViewTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")  # noqa: S106
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")

        self.post1 = Post.objects.create(title="Post 1", user=self.user)
        self.post2 = Post.objects.create(title="Post 2", user=self.user)

    def test_list_posts(self):
        url = reverse("posts:post-listcreate")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("total_ratings", response.data["results"][0])
        self.assertIn("avg_rating", response.data["results"][0])

    def test_create_post(self):
        url = reverse("posts:post-listcreate")
        data = {"title": "New Post", "body": "New Body"}
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], "New Post")


class RatingCreateViewTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")  # noqa: S106
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")

        self.post = Post.objects.create(title="Post with Rating", user=self.user)

    def test_create_rating(self):
        url = reverse("posts:rating-create", args=[self.post.id])
        data = {"score": 4}
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["score"], 4)

    def test_invalid_positive_rating(self):
        url = reverse("posts:rating-create", args=[self.post.id])
        data = {"score": 6}
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_negative_rating(self):
        url = reverse("posts:rating-create", args=[self.post.id])
        data = {"score": -1}
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class RefreshMaterializedViewTaskTests(TestCase):
    def test_refresh_materialized_view_task_execution_time(self):
        start_time = time.time()

        result = refresh_materialized_view.apply()
        result.get()

        end_time = time.time()
        elapsed_time = end_time - start_time

        self.assertLess(elapsed_time, 5, "Task took longer than 5 seconds to complete.")
        self.assertTrue(result.successful(), "Task did not complete successfully.")
