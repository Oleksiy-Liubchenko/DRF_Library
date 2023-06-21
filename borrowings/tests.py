from datetime import timedelta, date
from django.contrib.auth import get_user_model
from django.test import TestCase, RequestFactory
from django.urls import reverse
from rest_framework import status

from books.models import Books
from borrowings.models import Borrowing
from borrowings.views import BorrowingsViewSet
from borrowings.serializers import BorrowingsSerializer, BorrowingsListSerializer
from django.contrib.auth.models import User
from rest_framework.test import force_authenticate, APITestCase

User = get_user_model()
TOMORROW = date.today() + timedelta(days=1)


class BorrowingViewSetTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.view = BorrowingsViewSet.as_view({"get": "list"})
        self.user = User.objects.create_user(
            email="user@test.com",
            password="12345678"
        )
        self.admin = User.objects.create_superuser(
            email="admin@test.com",
            password="admin12345678"
        )
        self.book = Books.objects.create(
            title="Test book",
            author="Test author",
            cover="H",
            inventory=5,
            daily_fee=5.00
        )
        self.borrowing = Borrowing.objects.create(
            user=self.user,
            book=self.book,
            expected_return_date=TOMORROW
        )

        self.borrowing1 = Borrowing.objects.create(
            user=self.user,
            book=self.book,
            expected_return_date=TOMORROW,
            actual_return_date=date.today() - timedelta(days=1)
        )

        self.borrowing2 = Borrowing.objects.create(
            user=self.user,
            book=self.book,
            expected_return_date=date.today() - timedelta(days=1),
            actual_return_date=date.today() - timedelta(days=1)
        )

        self.borrowing3 = Borrowing.objects.create(
            user=self.admin,
            book=self.book,
            expected_return_date=TOMORROW
        )

    def test_list_authenticated_user(self):
        request = self.factory.get("/borrowings/")
        force_authenticate(request, user=self.user)
        response = self.view(request)

        self.assertEqual(response.status_code, 200)
        serializer = BorrowingsListSerializer(
            [self.borrowing],
            many=True,
            context={"request": request}
        )
        self.assertEqual(response.data[0], serializer.data[0])

    def test_list_not_authenticated_user(self):
        request = self.factory.get("borrowings/")
        response = self.view(request)

        self.assertEqual(response.status_code, 401)

    def test_create_borrowing_inventory_decreased(self):
        """After borrowing book inventory should decrease to one book"""
        init_inventory = self.book.inventory

        serializer = BorrowingsSerializer(
            data={
                "book": self.book.id,
                "expected_return_date": TOMORROW
            },
            context={"request": self.factory.get("/")}
        )
        serializer.context["request"].user = self.user
        serializer.is_valid()
        borrowing = serializer.save()

        self.assertEqual(borrowing.book.inventory, init_inventory - 1)

    def test_list_active_borrowings(self):
        url = reverse("borrowings:borrowing-list")
        request = self.factory.get(url, {"is_active": True})
        force_authenticate(request, user=self.user)
        response = self.view(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["id"], self.borrowing.id)

    def test_list_borrowings_by_user_id(self):
        url = reverse("borrowings:borrowing-list")
        request = self.factory.get(url, {"user_id": self.admin.id})
        force_authenticate(request, user=self.admin)
        response = self.view(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], self.borrowing3.id)


class BorrowingsReturnViewSetTest(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email="test@test.com",
            password="testpassword"
        )
        self.book = Books.objects.create(
            title="Test Book",
            author="Test Author",
            cover="H",
            inventory=5,
            daily_fee=5.00
        )
        self.borrowing = Borrowing.objects.create(
            user=self.user,
            book=self.book,
            expected_return_date=TOMORROW
        )

    def test_return_book_inventory_increase(self):
        """After book returned book inventory should increase to one book"""
        url = reverse(
            "borrowings:borrowings-return",
            kwargs={"pk": self.borrowing.pk})
        self.client.force_authenticate(user=self.user)

        response = self.client.post(
            url,
            data={"actual_return_date": date.today()}
        )
        borrowing = Borrowing.objects.get(pk=self.borrowing.pk)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIsNotNone(borrowing.actual_return_date)
        self.assertEqual(borrowing.book.inventory, 6)

        response = self.client.post(url, data={"actual_return_date": date.today()})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        borrowing.refresh_from_db()
        self.assertEqual(borrowing.book.inventory, 6)

    def test_return_book_twice(self):
        """Book can't be returned twice if was only one borrowing"""
        url = reverse("borrowings:borrowings-return", kwargs={"pk": self.borrowing.pk})
        self.client.force_authenticate(user=self.user)

        response = self.client.post(url, data={"actual_return_date": date.today()})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # second attempt
        response = self.client.post(url, data={"actual_return_date": date.today()})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        borrowing = Borrowing.objects.get(pk=self.borrowing.pk)
        self.assertEqual(borrowing.book.inventory, 6)
