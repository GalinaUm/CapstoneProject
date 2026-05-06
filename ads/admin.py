from django.contrib import admin

from .models import Ad


@admin.register(Ad)
class AdAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "price", "get_reviews_count", "created_at")
    search_fields = ("title", "author")
    ordering = ("-created_at",)
    list_filter = ("author",)

    def get_queryset(self, request):
        from django.db.models import Count

        queryset = super().get_queryset(request)
        return queryset.annotate(_reviews_count=Count("reviews"))

    def get_reviews_count(self, obj):
        return obj.reviews_count()

    get_reviews_count.short_description = "Отзывы"
    get_reviews_count.admin_order_field = "_reviews_count"
