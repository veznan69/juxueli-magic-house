"""预约看房模型：租客发起 → 房东确认/拒绝 → 完成。"""
from django.conf import settings
from django.db import models

from apps.house.models import House


class Appointment(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending', '待确认'
        CONFIRMED = 'confirmed', '已确认'
        REJECTED = 'rejected', '已拒绝'
        DONE = 'done', '已完成'

    house = models.ForeignKey(House, on_delete=models.CASCADE,
                              related_name='appointments', verbose_name='房源')
    tenant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                               related_name='appointments', verbose_name='租客')
    visit_time = models.DateTimeField('预约看房时间')
    phone = models.CharField('联系电话', max_length=20)
    remark = models.CharField('备注', max_length=200, blank=True, default='')
    status = models.CharField('状态', max_length=10, choices=Status.choices,
                              default=Status.PENDING)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        verbose_name = '预约看房'
        verbose_name_plural = '预约看房'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.tenant.username} 预约 {self.house.title}（{self.get_status_display()}）'
