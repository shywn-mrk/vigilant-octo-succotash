from django.urls import path

from .views import PostListCreateView
from .views import RatingCreateView

urlpatterns = [
    path("", PostListCreateView.as_view(), name="post-listcreate"),
    path("<int:id>/rate/", RatingCreateView.as_view(), name="rating-create"),
]

app_name = "posts"
