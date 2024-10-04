from rest_framework import serializers

from .models import Bill, BookingManage, Client, Room, Staff, StaffSchedule


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = "__all__"
        
class StaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = "__all__"
        
class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = "__all__"
        
class StaffScheduleSerializer(serializers.ModelSerializer):
    work_time = serializers.SerializerMethodField()
    close_case = serializers.SerializerMethodField()
    class Meta:
        model = StaffSchedule
        fields = "__all__"
    def get_work_time(self, obj):
        return obj.work_time()
    
    def get_close_case(self, obj):
        return obj.close_case()
        
class BookingManageSerializer(serializers.ModelSerializer):
    staff = serializers.CharField(source='staff.username', read_only=True)
    class Meta:
        model = BookingManage
        fields = "__all__"
        
class BillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bill
        fields = "__all__"