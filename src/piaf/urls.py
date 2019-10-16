from django.urls import path

from .views import IndexView, ParagraphApi, AdminView
from .api import MeView


app_name = "app"

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("admin", AdminView.as_view(), name="admin"),
    path("api/paragraph", ParagraphApi.as_view(), name="api_paragraph"),
    path("me", MeView.as_view(), name="me"),
]
