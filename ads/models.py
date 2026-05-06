from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Ad(models.Model):
    title = models.CharField(
        max_length=200,
        verbose_name="Заголовок",
        help_text="Укажите заголовок",
    )
    price = models.PositiveIntegerField(
        default=0,
        verbose_name="Цена",
        help_text="Укажите цену",
    )
    description = models.TextField(
        max_length=1000,
        null=True,
        blank=True,
        verbose_name="Описание",
        help_text="Укажите описание",
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="ads",
        verbose_name="Автор",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания",
    )
    image = models.ImageField(
        upload_to="ads/images/", null=True, blank=True, verbose_name="Изображение"
    )

    class Meta:
        verbose_name = "Объявление"
        verbose_name_plural = "Объявления"
        ordering = ("-created_at",)

    def __str__(self):
        return self.title


class Review(models.Model):
    text = models.TextField(
        max_length=1000,
        verbose_name="Текст отзыва",
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Автор отзыва",
        related_name="reviews",
    )
    ad = models.ForeignKey(
        Ad,
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name="Объявление",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания",
    )
    rating = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5),
        ],
        verbose_name="Оценка",
        help_text="Поставьте оценку от 1 до 5",
    )

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        unique_together = ("ad", "author")
        ordering = ("-created_at",)
