from django.contrib import admin


class BaseModelAdmin(admin.ModelAdmin):
    readonly_fields = ["created_at", "updated_at"]
    list_per_page = 30
