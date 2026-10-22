"""公告模型：管理员发布，全员可见。"""
from django.conf import settings
from django.db import models


class Notice(models.Model):
    title = models.CharField('标题', max_length=100)
    content = models.TextField('内容')
    publisher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
                                  related_name='notices', verbose_name='发布人',
                                  null=True, blank=True)
    created_at = models.DateTimeField('发布时间', auto_now_add=True)

    class Meta:
        verbose_name = '公告'
        verbose_name_plural = '公告'
        ordering = ['-created_at']

    def __str__(self):
        return self.title
