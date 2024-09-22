from django.contrib import admin

from .models import Bill, BookingManage, Client, Room, Staff, StaffSchedule

admin.site.register(Room)
admin.site.register(Client)
admin.site.register(Staff)
admin.site.register(StaffSchedule)
admin.site.register(BookingManage)
admin.site.register(Bill)
