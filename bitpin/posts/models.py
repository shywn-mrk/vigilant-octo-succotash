from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator
from django.core.validators import MinValueValidator
from django.db import models

from bitpin.base.models import BaseModle

User = get_user_model()


class Post(BaseModle):
    """
    Post model

    Attributes:
    - title: str
    - body: str

    Methods:
    - __str__: str
    """

    title = models.CharField(max_length=255)
    body = models.TextField()

    def __str__(self):
        return self.title


class Rating(BaseModle):
    """
    Rating model

    Attributes:
    - user: User
    - post: Post
    - score: int

    Methods:
    - __str__: str
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    score = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])

    class Meta:
        unique_together = ["user", "post"]

    def __str__(self):
        return f"{self.user} - {self.post} - {self.score}"
