from rest_framework import viewsets
from rest_framework.decorators import action
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
