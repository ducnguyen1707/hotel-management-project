# Import các mô-đun cần thiết từ Django
from datetime import timedelta

from django.conf import \
    settings  # Import settings từ Django để truy cập cấu hình
from django.db import models  # Import models để định nghĩa các mô hình dữ liệu
from django.utils import timezone  # Import timezone để xử lý thời gian


# Hàm tải lên hình ảnh khách hàng
def client_pic_upload(instance, filename):
    return f"client/{instance.id}/client_pic/{filename}"

# Hàm tải lên hình ảnh nhân viên
def staff_pic_upload(instance, filename):
    return f"staff/{instance.id}/staff_pic/{filename}"

# Định nghĩa model Room - dùng để lưu trữ thông tin các phòng trong khách sạn
class Room(models.Model):
    ROOM_CATEGORY = [  # Các loại phòng
        ("Single", "Single"),
        ("Double", "Double"),
    ]

    ROOM_STATUS = [  # Trạng thái của phòng
        ("NOT READY", "NOT READY"),
        ("READY", "READY"),
    ]

    ROOM_PRICE = [  # Giá phòng
        ("200000", "200,000 VND"),
        ("300000", "300,000 VND"),
    ]

    room_number = models.IntegerField()  # Số phòng
    room_type = models.CharField(
        max_length=50, choices=ROOM_CATEGORY
    )  # Loại phòng (ví dụ: Deluxe, Standard)
    room_status = models.CharField(
        max_length=50, choices=ROOM_STATUS, default="NOT READY"
    )  # Trạng thái phòng
    description = models.CharField(
        max_length=250, null=True
    )  # Mô tả phòng (ví dụ: phòng có view biển)
    floor = models.IntegerField(null=True)  # Tầng của phòng
    price = models.CharField(
        max_length=50, choices=ROOM_PRICE
    )  # Giá phòng (sử dụng CharField cho giá trị số)

    # Hàm trả về chuỗi đại diện cho đối tượng Room
    def __str__(self):
        return f"Phòng số: {self.room_number}. Loại phòng: {self.room_type}. Mô tả: {self.description}. Giá niêm yết: {self.price}."

# Định nghĩa model Client - dùng để lưu trữ thông tin khách hàng
class Client(models.Model):
    name = models.CharField(max_length=50)  # Tên khách hàng
    id_number = models.CharField(
        max_length=12, unique=True, null=False
    )  # Số CCCD khách hàng, unique để không trùng lặp
    vehicle = models.CharField(
        max_length=50, null=True, blank=True
    )  # Phương tiện khách sử dụng (nếu có), có thể để trống
    age = models.IntegerField(
        null=True, blank=True
    )  # Tuổi của khách hàng, có thể để trống
    client_phone = models.CharField(max_length=12, null=True, blank=True)  # Số điện thoại khách hàng
    cccd_pic = models.FileField(upload_to=client_pic_upload, null=True, blank=True)  # Ảnh CCCD của khách

    # Hàm trả về chuỗi đại diện cho đối tượng Client
    def __str__(self):
        return f"Tên khách hàng: {self.name}. Số CCCD: {self.id_number}. SĐT khách hàng: {self.client_phone}"

# Định nghĩa model Staff - lưu trữ thông tin về nhân viên
class Staff(models.Model):
    account = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )  # Liên kết đến User model (tài khoản người dùng)
    position_name = models.CharField(
        max_length=50
    )  # Vị trí của nhân viên (ví dụ: Lễ tân, Quản lý)
    staff_phone = models.CharField(max_length=12, null=True, blank=True)  # Số điện thoại nhân viên
    staff_id_number = models.CharField(
        max_length=12, unique=True, null=True, blank=True
    )  # Số CCCD nhân viên
    staff_pic = models.FileField(upload_to=staff_pic_upload, null=True, blank=True)  # Ảnh nhân viên

    # Hàm trả về chuỗi đại diện cho đối tượng Staff
    def __str__(self):
        return f"Tên nhân viên: {self.account.username}. SĐT nhân viên: {self.staff_phone}"

# Định nghĩa model StaffSchedule - lưu trữ thông tin lịch làm việc của nhân viên
class StaffSchedule(models.Model):
    shift_name = models.CharField(max_length=50)  # Tên ca làm (ví dụ: Ca sáng, Ca tối)
    start_time = models.TimeField()  # Giờ bắt đầu ca làm
    end_time = models.TimeField()  # Giờ kết thúc ca làm
    date = models.DateField()  # Ngày làm việc
    staff = models.ManyToManyField(
        Staff
    )  # Liên kết nhiều nhân viên với nhiều ca làm (nhiều-nhiều)

    # Hàm trả về chuỗi đại diện cho đối tượng StaffSchedule
    def __str__(self):
        return f"Lịch làm: {self.shift_name}"

    # Hàm tính thời gian làm việc
    def work_time(self):
        start = timedelta(hours=self.start_time.hour, minutes=self.start_time.minute)  # Thời gian bắt đầu
        end = timedelta(hours=self.end_time.hour, minutes=self.end_time.minute)  # Thời gian kết thúc
        x = end - start  # Tính thời gian làm việc
        total_h = x.total_seconds() // 3600  # Tổng số giờ
        total_m = (x.total_seconds() % 3600) // 60  # Tổng số phút
        if total_h > 2:  # Nếu tổng giờ làm việc lớn hơn 2
            return {
                "message": "Hãy uống nhiều nước và giữ tỉnh táo khi làm việc bạn nhé"
            }
        return f"{int(total_h)} giờ {int(total_m)} phút"  # Trả về thời gian làm việc

    # Hàm kiểm tra tình trạng làm việc
    def close_case(self):
        now = timezone.now().time()  # Lấy thời gian hiện tại
        end = self.end_time  # Thời gian kết thúc ca
        if now >= end:  # Nếu thời gian hiện tại lớn hơn hoặc bằng thời gian kết thúc
            return f"Cảm ơn bạn vì đã làm việc một cách năng động"
        return f"Cố gắng lên nào, bạn đang trong thời gian ca làm nhé"

# Định nghĩa model BookingManage - quản lý việc đặt phòng
class BookingManage(models.Model):
    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name="booking_client",
        null=True,
        blank=True,
    )  # Liên kết 1-1 với khách hàng (ForeignKey), cho phép bỏ trống
    room = models.ManyToManyField(
        Room, related_name="booking_room"
    )  # Liên kết nhiều phòng với một booking
    check_in_time = models.DateTimeField()  # Thời gian check-in
    check_out_time = models.DateTimeField()  # Thời gian check-out
    staff = models.ForeignKey(
        Staff,
        on_delete=models.CASCADE,
        related_name="booking_staff",
        null=True,
        blank=True,
    )  # Nhân viên quản lý booking

    # Hàm kiểm tra trạng thái phòng
    def check_room_status(self):
        for room in self.room.all():  # Duyệt qua tất cả các phòng trong booking
            if BookingManage.objects.filter(
                room=room,
                check_in_time__lt=self.check_out_time,
                check_out_time__gt=self.check_in_time,
            ).exists():  # Kiểm tra nếu phòng đã được đặt trong khoảng thời gian này
                return False  # Phòng không còn khả dụng
        return True  # Phòng còn khả dụng

    # Hàm lưu thông tin booking
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Lưu thông tin booking
        for room in self.room.all():  # Cập nhật trạng thái phòng
            if self.check_out_time <= timezone.now():  # Nếu thời gian check-out đã qua
                room.room_status = "READY"  # Đặt trạng thái phòng là sẵn sàng
            else:
                room.room_status = "NOT READY"  # Đặt trạng thái phòng là không sẵn sàng
            room.save()  # Lưu thay đổi trạng thái phòng

# Định nghĩa model Bill - quản lý hóa đơn cho mỗi booking
class Bill(models.Model):
    booking_info = models.OneToOneField(
        BookingManage, on_delete=models.CASCADE
    )  # Liên kết 1-1 với BookingManage
    tax = models.FloatField(default=0.1)  # Mức thuế, mặc định là 10%
    paid = models.BooleanField(default=False)  # Trạng thái thanh toán

    # Hàm tính tổng giá trị phòng sau thuế
    def price_after_tax(self):
        rooms = self.booking_info.room.all()  # Lấy tất cả các phòng từ booking_info
        room_price = sum(
            room.price for room in rooms
        )  # Tính tổng giá trị của tất cả các phòng
        total = room_price + (room_price * self.tax)  # Cộng tổng tiền phòng với thuế
        return total  # Trả về tổng giá trị sau thuế
