from django.contrib.auth import get_user_model
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from user.serizlizers import UserSerializer


class CreateUserView(generics.CreateAPIView):
    """Creating new user with *email, *password, first_name, last_name"""
    serializer_class = UserSerializer


class ManagingUser(generics.RetrieveUpdateAPIView):
    """User profile with managing info opportunity"""

    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user


class UsersListView(APIView):
    """List of all users for users who have is_staff = True"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if not request.user.is_staff:
            return Response(
                {"detail": "User is not staff"},
                status=status.HTTP_403_FORBIDDEN
            )
        users = get_user_model().objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
