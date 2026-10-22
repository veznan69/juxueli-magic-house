"""演示数据种子命令：python manage.py seed_demo（幂等，可重复执行）。"""
from datetime import date, datetime, timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from apps.appointment.models import Appointment
from apps.bill.models import Bill
from apps.contract.models import Contract
from apps.favorite.models import Favorite
from apps.house.models import House
from apps.lessor.models import Lessor
from apps.notice.models import Notice
from apps.repair.models import Repair
from apps.users.models import User


HOUSES = [
    # (标题, 区域, 地址, 户型, 面积, 月租, 押金, 押付, 配套, 状态, 出租方)
    ('阳光南向一居室 近地铁口', '朝阳区', '望京西园三区 12 号楼 2 单元 501', '1室1厅',
     45.0, 3200, 3200, '押一付三', 'WiFi,空调,洗衣机,冰箱,热水器', 'available', 0),
    ('精装两居 拎包入住 家电齐全', '朝阳区', '常营中路 3 号院 6 号楼 1802', '2室1厅',
     78.0, 4800, 4800, '押一付三', 'WiFi,空调,洗衣机,冰箱,电视,床垫', 'available', 0),
    ('整租三室两卫 适合合租', '海淀区', '西二旗智学苑 9 号楼 703', '3室2厅',
     118.0, 7200, 7200, '押一付一', 'WiFi,空调,洗衣机,冰箱,车位', 'available', 1),
    ('温馨小两居 采光好 周边成熟', '海淀区', '学院路 15 号院 4 号楼 1104', '2室1厅',
     72.0, 5100, 5100, '押一付三', 'WiFi,空调,洗衣机,冰箱,热水器', 'available', 1),
    ('白领公寓单间 独立卫浴', '西城区', '广安门内大街 206 号楼 815', '1室0厅',
     28.0, 2600, 2600, '押一付一', 'WiFi,空调,公共厨房,洗衣机', 'available', 1),
    ('湖景两居 高楼层视野开阔', '朝阳区', '望京花园东区 3 号楼 2201', '2室2厅',
     89.0, 5600, 5600, '押一付三', 'WiFi,空调,地暖,冰箱,洗碗机', 'available', 0),
    ('老小区两居 价格实惠', '丰台区', '方庄芳城园一区 8 号楼 602', '2室1厅',
     65.0, 3900, 3900, '押一付三', 'WiFi,空调,洗衣机,冰箱', 'available', 0),
    ('学 区 两 居 紧邻名校', '海淀区', '中关村北一条 11 号楼 901', '2室1厅',
     76.0, 6300, 6300, '押一付三', 'WiFi,空调,洗衣机,冰箱,书桌', 'rented', 1),
    ('江景大平层四居室', '朝阳区', '朝阳门外大街 18 号楼 3001', '4室2厅',
     165.0, 9800, 9800, '押一付三', 'WiFi,中央空调,地暖,车位,健身房', 'rented', 0),
    ('一居室过渡过渡可选', '丰台区', '马家堡西路 36 号楼 1503', '1室1厅',
     41.0, 2900, 2900, '押一付一', 'WiFi,空调,洗衣机', 'pending', 1),
    ('朝南主卧带阳台 短租勿扰', '西城区', '白纸坊西街 22 号楼 906', '1室1厅',
     52.0, 3600, 3600, '押一付三', 'WiFi,空调,洗衣机,冰箱', 'offline', 0),
]


class Command(BaseCommand):
    help = '灌入演示数据：账号、出租方、房源、合同、账单、预约、收藏、报修、公告'

    def handle(self, *args, **options):
        # 1) 管理员（已存在则同步角色）
        admin, _ = User.objects.get_or_create(
            username='admin',
            defaults={'email': 'admin@example.com', 'role': User.Roles.ADMIN,
                      'is_staff': True, 'is_superuser': True})
        admin.role = User.Roles.ADMIN
        admin.is_staff = admin.is_superuser = True
        admin.set_password('admin123456')
        admin.save()

        # 2) 房东与租客账号
        landlord, _ = User.objects.get_or_create(
            username='landlord',
            defaults={'role': User.Roles.LANDLORD, 'phone': '13911112222'})
        landlord.role = User.Roles.LANDLORD
        landlord.set_password('landlord123')
        landlord.save()

        tenant1, _ = User.objects.get_or_create(
            username='tenant1', defaults={'role': User.Roles.TENANT,
                                          'phone': '13833334444'})
        tenant1.role = User.Roles.TENANT
        tenant1.set_password('tenant123')
        tenant1.save()

        tenant2, _ = User.objects.get_or_create(
            username='tenant2', defaults={'role': User.Roles.TENANT,
                                          'phone': '13855556666'})
        tenant2.role = User.Roles.TENANT
        tenant2.set_password('tenant123')
        tenant2.save()

        # 3) 出租主体（个人 + 公司）
        lessor_personal, _ = Lessor.objects.get_or_create(
            name='橙家公寓（个人房东）',
            defaults={'lessor_type': Lessor.LessorType.PERSONAL,
                      'contact_person': '王橙', 'phone': '13911112222'})
        lessor_company, _ = Lessor.objects.get_or_create(
            name='青柠房屋托管（公司）',
            defaults={'lessor_type': Lessor.LessorType.COMPANY,
                      'license_no': '91110105MA01XYZ99X',
                      'contact_person': '刘青', 'phone': '010-88886666',
                      'address': '朝阳区常营中路 3 号院底商 102'})
        landlord.lessors.add(lessor_personal, lessor_company)

        # 4) 房源
        lessors = [lessor_personal, lessor_company]
        houses = []
        for (title, district, address, rooms, area, rent, deposit, payment,
             facilities, status, li) in HOUSES:
            house, created = House.objects.get_or_create(
                title=title,
                defaults={'district': district, 'address': address,
                          'rooms': rooms, 'area': area, 'rent': rent,
                          'deposit': deposit, 'payment': payment,
                          'facilities': facilities, 'status': status,
                          'landlord': lessors[li],
                          'view_count': 37 * (len(houses) + 3)})
            houses.append(house)
            if created:
                self.stdout.write(f'  + 房源：{title}')

        available = [h for h in houses if h.status == House.Status.AVAILABLE]
        rented = [h for h in houses if h.status == House.Status.RENTED]

        # 5) 合同与账单（rented 房源各签一份）
        self._seed_contract(tenant1, rented[0], date(2026, 8, 1),
                            date(2027, 7, 31),
                            [('2026-08', Bill.Status.PAID),
                             ('2026-09', Bill.Status.PAID),
                             ('2026-10', Bill.Status.UNPAID)])
        self._seed_contract(tenant2, rented[1], date(2026, 9, 1),
                            date(2027, 8, 31),
                            [('2026-09', Bill.Status.PAID),
                             ('2026-10', Bill.Status.OVERDUE)])

        # 6) 预约 / 收藏 / 报修
        Appointment.objects.get_or_create(
            house=available[0], tenant=tenant2,
            defaults={'visit_time': timezone.now() + timedelta(days=2),
                      'phone': '13855556666', 'remark': '想周末下午看房'})
        Favorite.objects.get_or_create(user=tenant1, house=available[1])
        Favorite.objects.get_or_create(user=tenant1, house=available[3])
        Repair.objects.get_or_create(
            house=rented[0], tenant=tenant1,
            defaults={'category': '水电', 'description': '厨房水龙头漏水，关不紧',
                      'status': Repair.Status.PROCESSING,
                      'reply': '已联系师傅，周四上午上门'})
        Repair.objects.get_or_create(
            house=rented[1], tenant=tenant2,
            defaults={'category': '家电', 'description': '空调制冷效果差，可能缺氟'})

        # 7) 公告
        Notice.objects.get_or_create(
            title='平台上线公告',
            defaults={'publisher': admin,
                      'content': '房屋租赁管理系统正式上线！支持在线找房、预约看房、'
                                 '电子合同、租金缴纳与在线报修，祝大家租得安心。'})
        Notice.objects.get_or_create(
            title='中秋国庆租房指南',
            defaults={'publisher': admin,
                      'content': '节日期间看房需求旺盛，建议提前 3 天预约看房；'
                                 '签约请仔细核对租期、押付方式与账单周期。'})

        self.stdout.write(self.style.SUCCESS(
            f'演示数据就绪：房源 {House.objects.count()} 套 / 用户 {User.objects.count()} / '
            f'合同 {Contract.objects.count()} / 账单 {Bill.objects.count()}'))
        self.stdout.write('测试账号：admin/admin123456（管理员）、'
                          'landlord/landlord123（房东）、tenant1|tenant2/tenant123（租客）')

    def _seed_contract(self, tenant, house, start, end, bills):
        contract, created = Contract.objects.get_or_create(
            house=house, tenant=tenant,
            defaults={'start_date': start, 'end_date': end,
                      'monthly_rent': house.rent, 'deposit': house.deposit})
        for period, status in bills:
            Bill.objects.get_or_create(
                contract=contract, period=period,
                defaults={'amount': house.rent,
                          'due_date': date(int(period[:4]), int(period[5:]), 5),
                          'status': status,
                          'paid_at': (timezone.now() - timedelta(days=10))
                          if status == Bill.Status.PAID else None})
        if created:
            self.stdout.write(f'  + 合同：{tenant.username} × {house.title}')
