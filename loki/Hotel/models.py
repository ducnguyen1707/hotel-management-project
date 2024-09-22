# Import các mô-đun cần thiết từ Django
from django.conf import settings
from django.db import models


# Định nghĩa model Room - dùng để lưu trữ thông tin các phòng trong khách sạn
class Room(models.Model):
    room_number = models.IntegerField()  # Số phòng
    room_type = models.CharField(max_length=50)  # Loại phòng (ví dụ: Deluxe, Standard)
    description = models.CharField(max_length=250, null =True)  # Mô tả phòng (ví dụ: phòng có view biển)
    floor = models.IntegerField(null= True)  # Tầng của phòng
    price = models.IntegerField()  # Giá phòng (sử dụng IntegerField cho giá trị số)

    # Hàm trả về chuỗi đại diện cho đối tượng Room
    def __str__(self):
        return f"Phòng số: {self.room_number}. Loại phòng: {self.room_number}. Mô tả: {self.description}. Giá niêm yết: {self.price}."

# Định nghĩa model Client - dùng để lưu trữ thông tin khách hàng
class Client(models.Model):
    name = models.CharField(max_length=50)  # Tên khách hàng
    id_number = models.CharField(max_length=12, unique=True, null=False)  # Số CCCD khách hàng, unique để không trùng lặp
    vehicle = models.CharField(max_length=50, null=True, blank=True)  # Phương tiện khách sử dụng (nếu có), có thể để trống
    age = models.IntegerField(null=True, blank=True)  # Tuổi của khách hàng, có thể để trống
    client_phone = models.CharField(max_length=12, null=True, blank=True)    
    # Hàm trả về chuỗi đại diện cho đối tượng Client
    def __str__(self):
        return f"Tên khách hàng:{self.name}. Số CCCD: {self.id_number}. SĐT khách hàng: {self.client_phone}"

# Định nghĩa model Staff - lưu trữ thông tin về nhân viên
class Staff(models.Model):
    name = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Liên kết đến User model (tài khoản người dùng)
    position_name = models.CharField(max_length=50)  # Vị trí của nhân viên (ví dụ: Lễ tân, Quản lý)
    status = models.BooleanField()  # Trạng thái làm việc của nhân viên (True: đang làm, False: nghỉ)
    staff_phone = models.CharField(max_length=12,null=True, blank=True)
    staff_id_number = models.CharField(max_length=12, unique=True, null= True, blank= True)
    
    # Hàm trả về chuỗi đại diện cho đối tượng Staff
    def __str__(self):
        return f"Tên nhân viên: {self.name.username}. SĐT nhân viên {self.staff_phone}"  # Sử dụng username từ User model

# Định nghĩa model StaffSchedule - lưu trữ thông tin lịch làm việc của nhân viên
class StaffSchedule(models.Model):
    shift_name = models.CharField(max_length=50)  # Tên ca làm (ví dụ: Ca sáng, Ca tối)
    start_time = models.TimeField()  # Giờ bắt đầu ca làm
    end_time = models.TimeField()  # Giờ kết thúc ca làm
    date = models.DateField()  # Ngày làm việc
    staff = models.ManyToManyField(Staff)  # Liên kết nhiều nhân viên với nhiều ca làm (nhiều-nhiều)

    # Hàm trả về chuỗi đại diện cho đối tượng StaffSchedule
    def __str__(self):
        return f"Lịch làm: {self.shift_name}"

# Định nghĩa model BookingManage - quản lý việc đặt phòng
class BookingManage(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="booking_client", null=True, blank=True)  
    # Liên kết 1-1 với khách hàng (ForeignKey), null=True và blank=True để cho phép bỏ trống với các bản ghi cũ
    room = models.ManyToManyField(Room, related_name="booking_room")  # Liên kết nhiều phòng với một booking
    check_in_time = models.DateTimeField()  # Thời gian check-in
    check_out_time = models.DateTimeField()  # Thời gian check-out
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE, related_name="booking_staff", null=True, blank=True)
    
    
# Định nghĩa model Bill - quản lý hóa đơn cho mỗi booking
class Bill(models.Model):
    booking_info = models.OneToOneField(BookingManage, on_delete=models.CASCADE)  # Liên kết 1-1 với BookingManage
    #tip = models.IntegerField(default=0)  # Trường cho tiền tip (hiện tại bị comment)
    tax = models.FloatField(default=0.1)  # Mức thuế, mặc định là 10%

    # Hàm tính tổng giá trị phòng sau thuế
    def price_after_tax(self):
        rooms = self.booking_info.room.all()  # Lấy tất cả các phòng từ booking_info
        room_price = sum(room.price for room in rooms)  # Tính tổng giá trị của tất cả các phòng
        
        # Cộng tổng tiền phòng với thuế
        total = room_price + (room_price * self.tax)
        
        return total  # Trả về tổng giá trị sau thuế
