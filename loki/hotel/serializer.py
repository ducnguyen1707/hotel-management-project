from rest_framework import serializers  # Import serializers từ DRF

from .models import (Bill, BookingManage,  # Import các model đã định nghĩa
                     Client, Room, Staff, StaffSchedule)


# Serializer cho Room
class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room  # Đặt model là Room
        fields = "__all__"  # Chọn tất cả các trường

    def to_representation(self, instance):
        representation = super().to_representation(instance)  # Gọi hàm cha để lấy đại diện
        representation["room_summary"] = str(
            instance
        )  # Sử dụng hàm __str__ để có chuỗi đại diện
        return representation  # Trả về đại diện đã được mở rộng


# Serializer cho Staff
class StaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff  # Đặt model là Staff
        fields = "__all__"  # Chọn tất cả các trường

    def to_representation(self, instance):
        representation = super().to_representation(instance)  # Gọi hàm cha để lấy đại diện
        representation["staff_summary"] = str(
            instance
        )  # Sử dụng hàm __str__ của model Staff
        return representation  # Trả về đại diện đã được mở rộng


# Serializer cho Client
class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client  # Đặt model là Client
        fields = "__all__"  # Chọn tất cả các trường

    def to_representation(self, instance):
        representation = super().to_representation(instance)  # Gọi hàm cha để lấy đại diện
        representation["client_summary"] = str(
            instance
        )  # Sử dụng hàm __str__ của model Client
        return representation  # Trả về đại diện đã được mở rộng


# Serializer cho StaffSchedule
class StaffScheduleSerializer(serializers.ModelSerializer):
    work_time = serializers.SerializerMethodField()  # Tạo trường tùy chỉnh cho thời gian làm việc
    close_case = serializers.SerializerMethodField()  # Tạo trường tùy chỉnh cho tình huống đóng
    staff = StaffSerializer(many=True)  # Sử dụng StaffSerializer để hiển thị danh sách nhân viên

    class Meta:
        model = StaffSchedule  # Đặt model là StaffSchedule
        fields = "__all__"  # Chọn tất cả các trường

    def get_work_time(self, obj):
        return obj.work_time()  # Gọi phương thức work_time từ đối tượng

    def get_close_case(self, obj):
        return obj.close_case()  # Gọi phương thức close_case từ đối tượng


# Serializer cho BookingManage
class BookingManageSerializer(serializers.ModelSerializer):
    check_room_status = serializers.SerializerMethodField()  # Tạo trường tùy chỉnh cho trạng thái phòng

    class Meta:
        model = BookingManage  # Đặt model là BookingManage
        fields = "__all__"  # Chọn tất cả các trường

    def get_room_status(self, obj):
        return obj.check_room_status()  # Gọi phương thức check_room_status từ đối tượng

    def create(self, validated_data):
        instance = super().create(validated_data)  # Gọi hàm cha để tạo đối tượng
        instance.save()  # Lưu đối tượng
        return instance  # Trả về đối tượng đã tạo


# Serializer cho Bill
class BillSerializer(serializers.ModelSerializer):
    price_after_tax = serializers.SerializerMethodField()  # Tạo trường tùy chỉnh cho giá sau thuế

    class Meta:
        model = Bill  # Đặt model là Bill
        fields = "__all__"  # Chọn tất cả các trường

    def get_price_after_tax(self, obj):
        return obj.price_after_tax()  # Gọi phương thức price_after_tax từ đối tượng
