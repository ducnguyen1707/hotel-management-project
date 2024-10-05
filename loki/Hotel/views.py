from django.shortcuts import render
from rest_framework import status, viewsets
from rest_framework.decorators import api_view
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response

from .models import Bill, BookingManage, Room, Staff, StaffSchedule
from .serializer import (BillSerializer, BookingManageSerializer,
                         RoomSerializer, StaffScheduleSerializer,
                         StaffSerializer)


# Create your views here.
class RoomViewSet(viewsets.ViewSet): 
    queryset = Room.objects.all()
    def list(self, request):
        room_id = request.query_params.get("id")
        room_number = request.query_params.get("room_number")
        room_status = request.query_params.get("room_status")
        if room_id:
            self.queryset = self.queryset.filter(id=room_id)
        if room_number:
            self.queryset= self.queryset.filter(room_number=room_number)
        if room_status:
            if room_status=="READY":
                self.queryset =  self.queryset.filter(room_status="READY")  
            elif room_status=="NOT READY":
                self.queryset = self.queryset.filter(room_status="NOT READY")
        serializer = RoomSerializer(self.queryset, many= True)
        return Response(serializer.data)
    def patch(self, request):
        try:
            id = request.query_params.get("id")
            item = Room.objects.get(id=id)
        except Room.DoesNotExist:
            return Response({"error": "Room not found."}, status=404)
        serializer = RoomSerializer(item, data=request.data, partial=True)
        
        if serializer.is_valid():
            room_status = request.data.get("room_status")
            price = request.data.get("price")
            #print(room_status, item)
            if room_status:
                item.room_status = room_status
                serializer.save()
            if price:
                item.price =price
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def put (self, request):
        id = request.query_parmas.get("id")
        room =Room.objects.get(id=id)
        serializer = RoomSerializer(room , data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
    def create(self, request):
        serializer = RoomSerializer(data = request.data)
        if serializer.is_valid():
            room = serializer.save()
        return Response(serializer.data)
    def delete(self, request):
        id = request.query_params.get("id")
        room = Room.objects.get(id=id)
        room.delete()
        return Response({"Room delete successfully"})

class StaffViewSet(viewsets.ViewSet):   
    queryset = Staff.objects.all()
    #serializer_class = StaffSerializer
    def list(self, request):
        staff = request.query_params.get("staff")=="true"
        position = request.query_params.get("position_name")
        phone = request.query_params.get("phone")
        staff_id = request.query_params.get("id")
        if staff and not request.user.is_autheticated:
            raise AuthenticationFailed()
        if staff_id:
            self.queryset =self.queryset.filter(id=staff_id )
        if position:
            self.queryset =self.queryset.filter(position_name=position)
        if phone:
            self.queryset = self.queryset.filter(staff_phone=phone)
        serializer = StaffSerializer(self.queryset, many =True)
        return Response(serializer.data)
    def patch(self,request):
        id = request.request_params.get("id")
        staff = Staff.objects.get(id=id)
        serializer = StaffSerializer(staff, data=request.data, partial=True)
        
        if serializer.is_valid():
            staff_phone = request.data.get("staff_phone")
            if staff_phone:
                staff.staff_phone = staff_phone
                serializer.save()
            return Response(serializer.data)
    def delete(self, request):
        staff_id= request.query_params.get("id")
        staff = Staff.objects.get(id=staff_id)
        staff.delete()
        return Response("Staff deleted successfully!")
        
class StaffScheduleViewSet(viewsets.ViewSet):
    queryset = StaffSchedule.objects.all()
   #serialize_class = StaffScheduleSerializer
    def list(self, request):
        id = request.query_params.get("id")
        name = request.query_params.get("name")
        staff = request.query_params.get("staff")=="true"
        shift_name =request.query_params.get("shift_name")
        if id:
            self.queryset = self.queryset.filter(id=id)
        if name:
            self.queryset = self.queryset.filter(shift_name=name)
        if staff:
            staff_id = request.user.id
            self.queryset = self.queryset.filter(staff=staff_id)
        if shift_name:
            self.queryset = self.queryset.filter(shift_name=shift_name)
        serializer = StaffScheduleSerializer(self.queryset, many=True)
        return Response(serializer.data)
    def create(self, request):
        serializer = StaffScheduleSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data)
    def put(self, request):
        id = request.query_params.get("id")
        schedule = StaffSchedule.objects.get(id=id)
        serializer = StaffScheduleSerializer(schedule, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
    def path(self, request):
        id = request.query_params.get("id")
        schedule = StaffSchedule.objects.get(id=id)
        serializer = StaffScheduleSerializer(schedule, data = request.data)
        if serializer.is_valid():
            start = request.data.get("start_time")
            end = request.data.get("end_time")
            if start and end:
                schedule.start_time = start
                schedule.end_time = end
                return Response(serializer.data)
    def delete(self, request):
        id = request.query_params.get("id")
        schedule = StaffSchedule.objects.get(id=id)
        schedule.delete()
        return Response("Schedule deleted successfully!")
    
class BookingManageViewSet(viewsets.ViewSet):
    queryset = BookingManage.objects.all()
    def list(self, request):
        id = request.query_params.get("id")
        client = request.query_params.get("client")
        staff = request.query_params.get("staff")
        if id:
            self.queryset = self.queryset.filter(id=id)
        if client:
            self.queryset = self.queryset.filter(client=client)
        if staff:
            self.queryset = self.queryset.filter(staff=staff)
        serializer = BookingManageSerializer(self.queryset, many=True)
        return Response(serializer.data)
    def put(self, request):
        id = request.query_params.get("id")
        book = BookingManage.objects.get(id=id)
        serializer =BookingManageSerializer(book, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
    def delete(self, request):
        id = request.query_params.get("id")
        book = BookingManage.objects.get(id=id)
        book.delete()
        return Response("Book deleted successfully!")
    
class BillViewSet(viewsets.ViewSet):
    queryset = Bill.objects.all()
    def list(self, request):
        id = request.query_params.get("id")
        staff = request.query_params.get("staff")
        client = request.query_params.get("client")
        if id:
            self.queryset = self.queryset.filter(id=id)
        if staff:
            self.queryset = self.queryset.filter(booking_info__staff=staff )
        if client:
            self.queryset = self.queryset.filter(booking_info__client=client)
        serializer = BillSerializer(self.queryset, many =True)
        return Response(serializer.data)
    def delete(self, request):
        id = request.query_params.get("id")
        bill = Bill.objects.get(id=id)
        bill.delete()
        return Response("Bill delete success")