from django.contrib import admin

from bitpin.base.admin import BaseModelAdmin

from .models import Post
from .models import Rating


@admin.register(Post)
class PostAdmin(BaseModelAdmin):
    list_display = ("title", "user", "created_at", "updated_at")
    search_fields = ["title", "body"]

    def has_add_permission(self, request):
        return request.user.is_staff

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(Rating)
class RatingAdmin(BaseModelAdmin):
    list_display = ("user", "post", "score", "created_at", "updated_at")

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False
