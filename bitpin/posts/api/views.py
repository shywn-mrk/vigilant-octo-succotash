from typing import Any

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.generics import CreateAPIView
from rest_framework.generics import ListAPIView
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.throttling import AnonRateThrottle
from rest_framework.throttling import UserRateThrottle

from bitpin.posts.models import Post
from bitpin.posts.models import Rating

from .serializers import PostSerializer
from .serializers import RatingSerializer


class PostListView(ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    throttle_classes = [AnonRateThrottle]

    @method_decorator(cache_page(60))
    def get(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        return super().get(request, *args, **kwargs)


class RatingCreateView(CreateAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]

    def get_serializer_context(self) -> dict[str, Any]:
        context = super().get_serializer_context()
        context["post"] = self.get_post()
        return context

    def get_post(self) -> Post:
        return get_object_or_404(Post, pk=self.kwargs.get("id"))

    def post(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_201_CREATED)

        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
