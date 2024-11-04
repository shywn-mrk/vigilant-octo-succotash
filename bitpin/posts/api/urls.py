from django.urls import path

from .views import PostListView
from .views import RatingCreateView

urlpatterns = [
    path("", PostListView.as_view(), name="post-list"),
    path("<int:id>/rate/", RatingCreateView.as_view(), name="rating-create"),
]

app_name = "posts"
