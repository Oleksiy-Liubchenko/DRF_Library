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
        """Creating instance with reassigned user"""
        user = self.context["request"].user
        validated_data["user"] = user
        borrowing = Borrowing.objects.create(**validated_data)

        return borrowing
