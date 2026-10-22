"""出租方（房东主体）模型：与登录账号解耦——个人房东 1 对 1，公司房东多账号共用。"""
from django.conf import settings
from django.db import models


class Lessor(models.Model):
    """出租主体：可以是个人、二房东，也可以是托管公司 / 中介。"""

    class LessorType(models.TextChoices):
        PERSONAL = 'personal', '个人房东'
        COMPANY = 'company', '公司/机构'

    name = models.CharField('名称（姓名/公司名）', max_length=100)
    lessor_type = models.CharField('类型', max_length=10,
                                   choices=LessorType.choices, default=LessorType.PERSONAL)
    license_no = models.CharField('营业执照号', max_length=50, blank=True, default='')
    contact_person = models.CharField('联系人', max_length=50)
    phone = models.CharField('联系电话', max_length=20)
    address = models.CharField('办公地址', max_length=200, blank=True, default='')
    operators = models.ManyToManyField(settings.AUTH_USER_MODEL, verbose_name='操作账号',
                                       related_name='lessors', blank=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        verbose_name = '出租方'
        verbose_name_plural = '出租方'

    def __str__(self):
        return f'{self.get_lessor_type_display()}·{self.name}'
