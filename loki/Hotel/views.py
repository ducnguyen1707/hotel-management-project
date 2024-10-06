from django.shortcuts import render  # Import render để hiển thị giao diện
from rest_framework import (status,  # Import các class và status từ DRF
                            viewsets)
from rest_framework.decorators import \
    api_view  # Import decorator để tạo API views
from rest_framework.exceptions import \
    AuthenticationFailed  # Import exception để xử lý lỗi xác thực
from rest_framework.response import \
    Response  # Import Response để trả về phản hồi JSON

from .models import (Bill, BookingManage,  # Import các model đã định nghĩa
                     Room, Staff, StaffSchedule)
from .serializer import StaffSerializer  # Import các serializer đã định nghĩa
from .serializer import (BillSerializer, BookingManageSerializer,
                         RoomSerializer, StaffScheduleSerializer)


# Tạo view cho Room
class RoomViewSet(viewsets.ViewSet):
    queryset = Room.objects.all()  # Lấy tất cả các phòng

    # Hiển thị danh sách phòng
    def list(self, request):
        room_id = request.query_params.get("id")  # Lấy ID phòng từ query params
        room_number = request.query_params.get("room_number")  # Lấy số phòng từ query params
        room_status = request.query_params.get("room_status")  # Lấy trạng thái phòng từ query params
        
        # Lọc phòng theo ID, số phòng và trạng thái
        if room_id:
            self.queryset = self.queryset.filter(id=room_id)
        if room_number:
            self.queryset = self.queryset.filter(room_number=room_number)
        if room_status:
            if room_status == "READY":
                self.queryset = self.queryset.filter(room_status="READY")
            elif room_status == "NOT READY":
                self.queryset = self.queryset.filter(room_status="NOT READY")
        
        serializer = RoomSerializer(self.queryset, many=True)  # Serialize danh sách phòng
        return Response(serializer.data)  # Trả về dữ liệu đã serialize

    # Cập nhật thông tin phòng
    def patch(self, request):
        try:
            id = request.query_params.get("id")  # Lấy ID phòng từ query params
            item = Room.objects.get(id=id)  # Lấy phòng theo ID
        except Room.DoesNotExist:
            return Response({"error": "Room not found."}, status=404)  # Xử lý trường hợp không tìm thấy phòng
        
        serializer = RoomSerializer(item, data=request.data, partial=True)  # Tạo serializer cho phòng
        
        # Kiểm tra tính hợp lệ của dữ liệu
        if serializer.is_valid():
            room_status = request.data.get("room_status")  # Lấy trạng thái phòng từ request
            price = request.data.get("price")  # Lấy giá phòng từ request
            
            # Cập nhật trạng thái phòng nếu có
            if room_status:
                item.room_status = room_status
                serializer.save()
            if price:
                item.price = price
                serializer.save()
            return Response(serializer.data)  # Trả về dữ liệu đã serialize
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # Trả về lỗi nếu không hợp lệ

    # Cập nhật toàn bộ thông tin phòng
    def put(self, request):
        id = request.query_params.get("id")  # Lấy ID phòng từ query params
        room = Room.objects.get(id=id)  # Lấy phòng theo ID
        serializer = RoomSerializer(room, data=request.data, partial=True)  # Tạo serializer cho phòng
        
        if serializer.is_valid():
            serializer.save()  # Lưu thông tin phòng
            return Response(serializer.data)  # Trả về dữ liệu đã serialize

    # Tạo phòng mới
    def create(self, request):
        serializer = RoomSerializer(data=request.data)  # Tạo serializer cho phòng mới
        if serializer.is_valid():
            room = serializer.save()  # Lưu thông tin phòng mới
        return Response(serializer.data)  # Trả về dữ liệu đã serialize

    # Xóa phòng
    def delete(self, request):
        id = request.query_params.get("id")  # Lấy ID phòng từ query params
        room = Room.objects.get(id=id)  # Lấy phòng theo ID
        room.delete()  # Xóa phòng
        return Response({"Room delete successfully"})  # Trả về thông báo thành công


# Tạo view cho Staff
class StaffViewSet(viewsets.ViewSet):
    queryset = Staff.objects.all()  # Lấy tất cả nhân viên

    def list(self, request):
        staff = request.query_params.get("staff") == "true"  # Kiểm tra nếu yêu cầu danh sách nhân viên
        position = request.query_params.get("position_name")  # Lấy vị trí từ query params
        phone = request.query_params.get("phone")  # Lấy số điện thoại từ query params
        staff_id = request.query_params.get("id")  # Lấy ID nhân viên từ query params
        
        # Kiểm tra xác thực người dùng nếu yêu cầu danh sách nhân viên
        if staff and not request.user.is_authenticated:
            raise AuthenticationFailed()  # Ném lỗi xác thực nếu không xác thực
        
        # Lọc nhân viên theo ID, vị trí và số điện thoại
        if staff_id:
            self.queryset = self.queryset.filter(id=staff_id)
        if position:
            self.queryset = self.queryset.filter(position_name=position)
        if phone:
            self.queryset = self.queryset.filter(staff_phone=phone)
        
        serializer = StaffSerializer(self.queryset, many=True)  # Serialize danh sách nhân viên
        return Response(serializer.data)  # Trả về dữ liệu đã serialize

    # Cập nhật thông tin nhân viên
    def patch(self, request):
        id = request.query_params.get("id")  # Lấy ID nhân viên từ query params
        staff = Staff.objects.get(id=id)  # Lấy nhân viên theo ID
        serializer = StaffSerializer(staff, data=request.data, partial=True)  # Tạo serializer cho nhân viên
        
        if serializer.is_valid():  # Kiểm tra tính hợp lệ của dữ liệu
            staff_phone = request.data.get("staff_phone")  # Lấy số điện thoại từ request
            if staff_phone:  # Cập nhật số điện thoại nếu có
                staff.staff_phone = staff_phone
                serializer.save()  # Lưu thông tin nhân viên
            return Response(serializer.data)  # Trả về dữ liệu đã serialize

    # Xóa nhân viên
    def delete(self, request):
        staff_id = request.query_params.get("id")  # Lấy ID nhân viên từ query params
        staff = Staff.objects.get(id=staff_id)  # Lấy nhân viên theo ID
        staff.delete()  # Xóa nhân viên
        return Response("Staff deleted successfully!")  # Trả về thông báo thành công


# Tạo view cho StaffSchedule
class StaffScheduleViewSet(viewsets.ViewSet):
    queryset = StaffSchedule.objects.all()  # Lấy tất cả lịch làm việc của nhân viên

    def list(self, request):
        id = request.query_params.get("id")  # Lấy ID lịch từ query params
        name = request.query_params.get("name")  # Lấy tên ca làm từ query params
        staff = request.query_params.get("staff") == "true"  # Kiểm tra nếu yêu cầu lịch làm của nhân viên
        shift_name = request.query_params.get("shift_name")  # Lấy tên ca làm từ query params
        
        # Lọc lịch làm việc theo ID, tên ca, và nhân viên
        if id:
            self.queryset = self.queryset.filter(id=id)
        if name:
            self.queryset = self.queryset.filter(shift_name=name)
        if staff:
            staff_id = request.user.id  # Lấy ID nhân viên từ người dùng đã xác thực
            self.queryset = self.queryset.filter(staff=staff_id)
        if shift_name:
            self.queryset = self.queryset.filter(shift_name=shift_name)
        
        serializer = StaffScheduleSerializer(self.queryset, many=True)  # Serialize danh sách lịch làm việc
        return Response(serializer.data)  # Trả về dữ liệu đã serialize

    # Tạo lịch làm việc mới
    def create(self, request):
        serializer = StaffScheduleSerializer(data=request.data)  # Tạo serializer cho lịch làm mới
        if serializer.is_valid():
            serializer.save()  # Lưu thông tin lịch làm
        return Response(serializer.data)  # Trả về dữ liệu đã serialize

    # Cập nhật toàn bộ thông tin lịch làm
    def put(self, request):
        id = request.query_params.get("id")  # Lấy ID lịch từ query params
        schedule = StaffSchedule.objects.get(id=id)  # Lấy lịch làm theo ID
        serializer = StaffScheduleSerializer(schedule, data=request.data)  # Tạo serializer cho lịch làm
        
        if serializer.is_valid():
            serializer.save()  # Lưu thông tin lịch làm
            return Response(serializer.data)  # Trả về dữ liệu đã serialize

    # Cập nhật một số trường của lịch làm
    def patch(self, request):
        id = request.query_params.get("id")  # Lấy ID lịch từ query params
        schedule = StaffSchedule.objects.get(id=id)  # Lấy lịch làm theo ID
        serializer = StaffScheduleSerializer(schedule, data=request.data)  # Tạo serializer cho lịch làm
        
        if serializer.is_valid():  # Kiểm tra tính hợp lệ của dữ liệu
            start = request.data.get("start_time")  # Lấy thời gian bắt đầu từ request
            end = request.data.get("end_time")  # Lấy thời gian kết thúc từ request
            
            # Cập nhật thời gian bắt đầu và kết thúc nếu có
            if start and end:
                schedule.start_time = start
                schedule.end_time = end
                serializer.save()  # Lưu thông tin lịch làm
                return Response(serializer.data)  # Trả về dữ liệu đã serialize

    # Xóa lịch làm việc
    def delete(self, request):
        id = request.query_params.get("id")  # Lấy ID lịch từ query params
        schedule = StaffSchedule.objects.get(id=id)  # Lấy lịch làm theo ID
        schedule.delete()  # Xóa lịch làm
        return Response("Schedule deleted successfully!")  # Trả về thông báo thành công


# Tạo view cho BookingManage
class BookingManageViewSet(viewsets.ViewSet):
    queryset = BookingManage.objects.all()  # Lấy tất cả các đặt phòng

    def list(self, request):
        id = request.query_params.get("id")  # Lấy ID đặt phòng từ query params
        client = request.query_params.get("client")  # Lấy ID khách hàng từ query params
        staff = request.query_params.get("staff")  # Lấy ID nhân viên từ query params
        
        # Lọc đặt phòng theo ID, khách hàng và nhân viên
        if id:
            self.queryset = self.queryset.filter(id=id)
        if client:
            self.queryset = self.queryset.filter(client=client)
        if staff:
            self.queryset = self.queryset.filter(staff=staff)
        
        serializer = BookingManageSerializer(self.queryset, many=True)  # Serialize danh sách đặt phòng
        return Response(serializer.data)  # Trả về dữ liệu đã serialize

    # Cập nhật thông tin đặt phòng
    def put(self, request):
        id = request.query_params.get("id")  # Lấy ID đặt phòng từ query params
        book = BookingManage.objects.get(id=id)  # Lấy đặt phòng theo ID
        serializer = BookingManageSerializer(book, data=request.data)  # Tạo serializer cho đặt phòng
        
        if serializer.is_valid():  # Kiểm tra tính hợp lệ của dữ liệu
            serializer.save()  # Lưu thông tin đặt phòng
            return Response(serializer.data)  # Trả về dữ liệu đã serialize

    # Xóa đặt phòng
    def delete(self, request):
        id = request.query_params.get("id")  # Lấy ID đặt phòng từ query params
        book = BookingManage.objects.get(id=id)  # Lấy đặt phòng theo ID
        book.delete()  # Xóa đặt phòng
        return Response("Book deleted successfully!")  # Trả về thông báo thành công


# Tạo view cho Bill
class BillViewSet(viewsets.ViewSet):
    queryset = Bill.objects.all()  # Lấy tất cả các hóa đơn

    def list(self, request):
        id = request.query_params.get("id")  # Lấy ID hóa đơn từ query params
        staff = request.query_params.get("staff")  # Lấy ID nhân viên từ query params
        client = request.query_params.get("client")  # Lấy ID khách hàng từ query params
        
        # Lọc hóa đơn theo ID, nhân viên và khách hàng
        if id:
            self.queryset = self.queryset.filter(id=id)
        if staff:
            self.queryset = self.queryset.filter(booking_info__staff=staff)
        if client:
            self.queryset = self.queryset.filter(booking_info__client=client)
        
        serializer = BillSerializer(self.queryset, many=True)  # Serialize danh sách hóa đơn
        return Response(serializer.data)  # Trả về dữ liệu đã serialize

    # Xóa hóa đơn
    def delete(self, request):
        id = request.query_params.get("id")  # Lấy ID hóa đơn từ query params
        bill = Bill.objects.get(id=id)  # Lấy hóa đơn theo ID
        bill.delete()  # Xóa hóa đơn
        return Response("Bill delete success")  # Trả về thông báo thành công

    # Cập nhật một số trường của hóa đơn
    def patch(self, request):
        id = request.query_params.get("id")  # Lấy ID hóa đơn từ query params
        bill = Bill.objects.get(id=id)  # Lấy hóa đơn theo ID
        serialize = BillSerializer(bill, data=request.data)  # Tạo serializer cho hóa đơn
        
        if serialize.is_valid():  # Kiểm tra tính hợp lệ của dữ liệu
            paid = request.data.get("paid")  # Lấy thông tin đã thanh toán từ request
            if paid is not None:  # Cập nhật thông tin đã thanh toán nếu có
                bill.paid = paid
            tax = request.data.get("tax")  # Lấy thông tin thuế từ request
            if tax is not None:  # Cập nhật thông tin thuế nếu có
                bill.tax = tax
            serialize.save()  # Lưu thông tin hóa đơn
            return Response(serialize.data)  # Trả về dữ liệu đã serialize
