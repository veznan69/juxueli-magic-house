"""房源模型与房源图片模型。"""
from django.db import models

from apps.lessor.models import Lessor


class House(models.Model):
    """房源表：外键关联出租方（而非登录账号），状态机：待审核/待租/已租/已下架。"""

    class Status(models.TextChoices):
        PENDING = 'pending', '待审核'
        AVAILABLE = 'available', '待租'
        RENTED = 'rented', '已租'
        OFFLINE = 'offline', '已下架'

    landlord = models.ForeignKey(Lessor, on_delete=models.CASCADE,
                                 related_name='houses', verbose_name='出租方')
    title = models.CharField('标题', max_length=100)
    district = models.CharField('所在区域', max_length=50)
    address = models.CharField('详细地址', max_length=200)
    rooms = models.CharField('户型', max_length=20, help_text='如：2室1厅')
    area = models.DecimalField('面积(㎡)', max_digits=7, decimal_places=1)
    rent = models.DecimalField('月租金(元)', max_digits=10, decimal_places=2)
    deposit = models.DecimalField('押金(元)', max_digits=10, decimal_places=2, default=0)
    payment = models.CharField('押付方式', max_length=20, default='押一付三')
    facilities = models.CharField('配套设施', max_length=200, blank=True, default='',
                                  help_text='逗号分隔，如：WiFi,空调,洗衣机')
    description = models.TextField('房源描述', blank=True, default='')
    status = models.CharField('状态', max_length=10, choices=Status.choices,
                              default=Status.AVAILABLE)
    view_count = models.PositiveIntegerField('浏览量', default=0)
    created_at = models.DateTimeField('发布时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = '房源'
        verbose_name_plural = '房源'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.title}（{self.get_status_display()}）'

    @property
    def cover_image(self):
        """封面图：优先取标记封面，否则取第一张。"""
        first = self.images.filter(is_cover=True).first() or self.images.first()
        return first.image.url if first and first.image else ''


class HouseImage(models.Model):
    """房源图片：一房多图，可标记封面。"""

    house = models.ForeignKey(House, on_delete=models.CASCADE,
                              related_name='images', verbose_name='房源')
    image = models.ImageField('图片', upload_to='houses/%Y/%m/')
    is_cover = models.BooleanField('是否封面', default=False)
    uploaded_at = models.DateTimeField('上传时间', auto_now_add=True)

    class Meta:
        verbose_name = '房源图片'
        verbose_name_plural = '房源图片'

    def __str__(self):
        return f'图片#{self.pk}（{self.house.title}）'
