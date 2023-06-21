from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from borrowings.models import Borrowing
from borrowings.serializers import (
    BorrowingsSerializer,
    BorrowingsListSerializer,
    BorrowingsReturnSerializer, BorrowingsDetailSerializer
)


class BorrowingsViewSet(viewsets.ModelViewSet):
    queryset = Borrowing.objects.all()
    model = Borrowing
    serializer_class = BorrowingsSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Two filters: 1) is_active means is book borrowing still active
        2) user_id allow admin to see all borrowings of any user"""

        is_active = self.request.query_params.get("is_active")
        user_id = self.request.query_params.get("user_id")
        queryset = self.queryset.filter(user=self.request.user)

        if self.request.user.is_staff:
            queryset = self.queryset.all()
            if user_id:
                queryset = queryset.filter(user_id=user_id)

        if is_active:
            queryset = queryset.filter(actual_return_date__isnull=True)

        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return BorrowingsListSerializer
        if self.action == "retrieve":
            return BorrowingsDetailSerializer
        if self.action == "return_book":
            return BorrowingsReturnSerializer
        return BorrowingsSerializer

    @action(detail=True, methods=["post"])
    def return_book(self, request, pk=None):
        borrowing = self.get_object()
        serializer = self.get_serializer(borrowing, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="is_active",
                description="Filtering is book still in active(borrowing status)",
                required=False,
                type=bool
            ),
            OpenApiParameter(
                name="user_id",
                description="Filtering by user id (only for admins) "
                            "to see borrowings of concreate user",
                required=False,
                type=int
            )
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
