from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from books.models import Books


class BooksViewSetTests(APITestCase):
    def setUp(self):
        self.book = Books.objects.create(
            title="Test Book",
            author="Test Author",
            cover="H",
            inventory=5,
            daily_fee=1.99
        )

    def test_list_books(self):
        url = reverse("books:books-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], self.book.title)

    def test_retrieve_book(self):
        url = reverse("books:books-detail", args=[self.book.pk])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], self.book.title)


class AdminBookApiTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "admin@admin.com",
            "12345678",
            is_staff=True,
        )
        self.client.force_authenticate(self.user)
        self.book = Books.objects.create(
            title="Test Book",
            author="Test Author",
            cover="H",
            inventory=5,
            daily_fee=1.99
        )

    def test_create_book(self):
        url = reverse("books:books-list")
        data = {
            "title": "Test book",
            "author": "Test author",
            "cover": "H",
            "inventory": 5,
            "daily_fee": "1.99",
        }

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_delete_book(self):
        url = reverse("books:books-detail", args=[self.book.pk])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
