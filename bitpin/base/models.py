from django.db import models
from django.utils import timezone


class BaseModle(models.Model):
    """
    BaseModel

    Attributes:
    - created_at: datetime
    - updated_at: datetime
    """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.pk:
            self.created_at = timezone.now()

        self.updated_at = timezone.now()

        super().save(*args, **kwargs)
