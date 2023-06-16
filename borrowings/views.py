from rest_framework import viewsets

from borrowings.models import Borrowing
from borrowings.serializers import (
    BorrowingsSerializer,
    BorrowingsListSerializer,
    BorrowingsDetailSerializer
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
        return BorrowingsSerializer
