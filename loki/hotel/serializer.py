from rest_framework import serializers

from .models import Bill, BookingManage, Client, Room, Staff, StaffSchedule


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = "__all__"
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['room_summary'] = str(instance)  # Sử dụng hàm __str__ để có chuỗi đại diện
        return representation
    
class StaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = "__all__"
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['staff_summary'] = str(instance)  # Sử dụng hàm __str__ của model Staff
        return representation
    
class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = "__all__"
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['client_summary'] = str(instance)  # Sử dụng hàm __str__ của model Client
        return representation
    
class StaffScheduleSerializer(serializers.ModelSerializer):
    work_time = serializers.SerializerMethodField()
    close_case = serializers.SerializerMethodField()
    staff = StaffSerializer( many=True)
    class Meta:
        model = StaffSchedule
        fields = "__all__"
    def get_work_time(self, obj):
        return obj.work_time()
    def get_close_case(self, obj):
        return obj.close_case()
        
class BookingManageSerializer(serializers.ModelSerializer):
    check_room_status = serializers.SerializerMethodField()
    class Meta:
        model = BookingManage
        fields = "__all__"    
    def get_room_status(self,obj):
        return obj.check_room_status()
    def create(self, validated_data):
        instance = super().create(validated_data)
        instance.save()
        return instance
    
class BillSerializer(serializers.ModelSerializer):
    price_after_tax =serializers.SerializerMethodField()
    class Meta:
        model = Bill
        fields = "__all__"
    def get_price_after_tax(self, obj):
        return obj.price_after_tax()