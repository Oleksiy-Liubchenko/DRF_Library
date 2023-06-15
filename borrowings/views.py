from rest_framework import viewsets

from borrowings.models import Borrowing
from borrowings.serializers import BorrowingsSerializer


class BorrowingsViewSet(viewsets.ModelViewSet):
    queryset = Borrowing.objects.all()
    model = Borrowing
    serializer_class = BorrowingsSerializer
