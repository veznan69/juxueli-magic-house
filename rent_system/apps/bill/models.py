"""租金账单模型：每份合同按月生成账单，记录缴费状态与时间。"""
from django.db import models

from apps.contract.models import Contract


class Bill(models.Model):
    class Status(models.TextChoices):
        UNPAID = 'unpaid', '待缴'
        PAID = 'paid', '已缴'
        OVERDUE = 'overdue', '逾期'

    contract = models.ForeignKey(Contract, on_delete=models.CASCADE,
                                 related_name='bills', verbose_name='所属合同')
    period = models.CharField('账期', max_length=20, help_text='如：2026-10')
    amount = models.DecimalField('应缴金额(元)', max_digits=10, decimal_places=2)
    due_date = models.DateField('应缴日期')
    status = models.CharField('缴费状态', max_length=10, choices=Status.choices,
                              default=Status.UNPAID)
    paid_at = models.DateTimeField('缴费时间', null=True, blank=True)

    class Meta:
        verbose_name = '租金账单'
        verbose_name_plural = '租金账单'
        ordering = ['-due_date']

    def __str__(self):
        return f'账单 {self.period} ¥{self.amount}（{self.get_status_display()}）'
