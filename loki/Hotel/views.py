from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response

from .models import Room, Staff
from .serializer import RoomSerializer, StaffSerializer


# Create your views here.
class RoomListViewSet(viewsets.ViewSet): 
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    
    def list(self, request):
        room_number = request.query_params.get("room_number")
        
        if room_number:
            self.queryset= self.queryset.filter(room_number=room_number)
            
        serializer = RoomSerializer(self.queryset, many= True)
        return Response(serializer.data)


class StaffListViewSet(viewsets.ViewSet):
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer
    
    def list(self, request):
        staff_name = request.query_params.get("name")
        position = request.query_params.get("position_name")
        
        if staff_name:
            self.queryset =self.queryset.filter(name__username=staff_name)
            
        if position:
            self.queryset =self.queryset.filter(position_name=position)
            
        serializer = StaffSerializer(self.queryset, many =True)
        return Response(serializer.data)
        
       