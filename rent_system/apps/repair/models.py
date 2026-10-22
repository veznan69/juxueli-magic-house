"""报修工单模型：租客提交 → 房东处理并反馈。"""
from django.conf import settings
from django.db import models

from apps.house.models import House


class Repair(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending', '待处理'
        PROCESSING = 'processing', '处理中'
        DONE = 'done', '已完成'

    house = models.ForeignKey(House, on_delete=models.CASCADE,
                              related_name='repairs', verbose_name='房源')
    tenant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                               related_name='repairs', verbose_name='报修人')
    category = models.CharField('报修类型', max_length=20,
                                choices=[('水电', '水电'), ('门窗', '门窗'),
                                         ('家电', '家电'), ('家具', '家具'), ('其他', '其他')])
    description = models.TextField('问题描述')
    status = models.CharField('状态', max_length=10, choices=Status.choices,
                              default=Status.PENDING)
    reply = models.TextField('处理反馈', blank=True, default='')
    created_at = models.DateTimeField('提交时间', auto_now_add=True)
    finished_at = models.DateTimeField('完成时间', null=True, blank=True)

    class Meta:
        verbose_name = '报修工单'
        verbose_name_plural = '报修工单'
        ordering = ['-created_at']

    def __str__(self):
        return f'报修#{self.pk} {self.house.title}（{self.get_status_display()}）'
