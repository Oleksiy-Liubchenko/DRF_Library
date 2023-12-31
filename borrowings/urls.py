from django.urls import path, include
from rest_framework import routers

from borrowings.views import BorrowingsViewSet

router = routers.DefaultRouter()
router.register("borrowings", BorrowingsViewSet)

urlpatterns = [
    path(
        "borrowings/<int:pk>/return/",
        BorrowingsViewSet.as_view({"post": "return_book"}),
        name="borrowings-return"
    ),
    path("", include(router.urls)),

]

app_name = "borrowings"
