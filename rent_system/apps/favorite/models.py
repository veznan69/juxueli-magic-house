"""收藏模型：租客与房源多对多（带收藏时间）。"""
from django.conf import settings
from django.db import models

from apps.house.models import House


class Favorite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                             related_name='favorites', verbose_name='租客')
    house = models.ForeignKey(House, on_delete=models.CASCADE,
                              related_name='favorited_by', verbose_name='房源')
    created_at = models.DateTimeField('收藏时间', auto_now_add=True)

    class Meta:
        verbose_name = '收藏'
        verbose_name_plural = '收藏'
        unique_together = ('user', 'house')
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user.username} 收藏 {self.house.title}'
