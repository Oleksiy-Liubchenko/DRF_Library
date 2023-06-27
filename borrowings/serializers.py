import datetime

from rest_framework import serializers

from borrowings.models import Borrowing
from telegram_bot.bot_send_message import send_telegram_message_when_borrowing


class BorrowingsSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Borrowing
        fields = (
            "id",
            "borrow_date",
            "expected_return_date",
            "book",
            "user"
        )

    def get_user(self, obj: Borrowing) -> int:
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

            message = f"New borrowing created: {borrowing.book.title} by {borrowing.user.email}"
            send_telegram_message_when_borrowing(message)

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


class BorrowingsReturnSerializer(serializers.ModelSerializer):
    """Update book inventory count when user return book.
    On book return page only allow to press "post",
    then actual_return_date will be today date
    """

    class Meta:
        model = Borrowing
        fields = ("id", "actual_return_date",)
        read_only_fields = ("actual_return_date",)

    def update(self, instance, validated_data):
        if instance.actual_return_date:
            raise serializers.ValidationError("This book has already been returned")

        instance.actual_return_date = datetime.date.today()
        instance.save()

        book = instance.book
        book.inventory += 1
        book.save()

        return instance
