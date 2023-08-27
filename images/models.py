from django.db import models
from django.conf import settings
from django.utils.text import slugify


class Image(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="image_created",
        on_delete=models.CASCADE
    )
    title = models.CharField(max_length=256)
    slug = models.SlugField(
        max_length=200,
        blank=True
    )
    url = models.URLField()
    image = models.ImageField(upload_to="images/%Y/%m/%d/")
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['-created']),
        ]
        ordering = ['-created']

    def __str__(self):
        return self.title

    # Автоматическая генерация slug'а из названия, если создан при генерации изображения
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, *kwargs)