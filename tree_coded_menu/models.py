from django.db import models
from django.urls import reverse

from config.logger import logger


class MenuItem(models.Model):
    name = models.CharField(max_length=255)
    parent = models.ForeignKey(
        "self", null=True, blank=True, on_delete=models.CASCADE, related_name="children"
    )
    url = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Может быть задан явным образом или как именованный URL",
    )
    named_url = models.CharField(
        max_length=100, blank=True, null=True, help_text="Именованный URL (например, 'main:index')"
    )
    menu_name = models.CharField(
        max_length=50, help_text="Название меню, чтобы различать несколько меню на странице"
    )

    class Meta:
        verbose_name = "Пункт меню"
        verbose_name_plural = "Пункты меню"

    def __str__(self):
        return self.name

    def get_url(self):
        """Возвращает URL пункта меню. Приоритет у named_url"""
        if self.named_url:
            try:
                return reverse(self.named_url)
            except Exception as e:
                logger.error(f"Failed to get named url: {str(e)}")
                return "#"
        return self.url or "#"
