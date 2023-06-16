from rest_framework import serializers

from borrowings.models import Borrowing


class BorrowingsSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Borrowing
        fields = (
            "id",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book",
            "user"
        )

    def get_user(self, obj):
        """Reassign user for borrowing book
        (instead user could borrow book not
         for himself, for user 2 for ex)"""

        user = self.context["request"].user
        return user.id

    def create(self, validated_data):
        """Creating instance with reassigned user.
        Also check is library have book inventory for borrowing"""

        user = self.context["request"].user
        book = validated_data["book"]

        if book.inventory > 0:
            book.inventory -= 1
            book.save()

            validated_data["user"] = user
            borrowing = Borrowing.objects.create(**validated_data)

            return borrowing
        raise serializers.ValidationError("No inventory for this book")


class BorrowingsListSerializer(BorrowingsSerializer):
    book = serializers.CharField(source="book.title")
    user = serializers.CharField(source="user.email")

    class Meta:
        model = Borrowing
        fields = (
            "id",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book",
            "user"
        )


class BorrowingsDetailSerializer(BorrowingsListSerializer):
    class Meta:
        model = Borrowing
        fields = "__all__"
