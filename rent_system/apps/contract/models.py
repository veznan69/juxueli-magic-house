"""租赁合同模型：关联房源与租客，按月生成账单。"""
from django.conf import settings
from django.db import models

from apps.house.models import House


class Contract(models.Model):
    class Status(models.TextChoices):
        ACTIVE = 'active', '履行中'
        EXPIRED = 'expired', '已到期'
        TERMINATED = 'terminated', '已解约'

    house = models.ForeignKey(House, on_delete=models.CASCADE,
                              related_name='contracts', verbose_name='房源')
    tenant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                               related_name='contracts', verbose_name='租客')
    start_date = models.DateField('起租日')
    end_date = models.DateField('到期日')
    monthly_rent = models.DecimalField('月租金(元)', max_digits=10, decimal_places=2)
    deposit = models.DecimalField('押金(元)', max_digits=10, decimal_places=2, default=0)
    status = models.CharField('状态', max_length=12, choices=Status.choices,
                              default=Status.ACTIVE)
    created_at = models.DateTimeField('签订时间', auto_now_add=True)

    class Meta:
        verbose_name = '租赁合同'
        verbose_name_plural = '租赁合同'
        ordering = ['-created_at']

    def __str__(self):
        return f'合同#{self.pk} {self.house.title}（{self.get_status_display()}）'
