"""
URL configuration for the Loki project.

The `urlpatterns` list routes URLs to views. For more information, please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views:
    1. Add an import: from my_app import views
    2. Add a URL to urlpatterns: path('', views.home, name='home')
Class-based views:
    1. Add an import: from other_app.views import Home
    2. Add a URL to urlpatterns: path('', Home.as_view(), name='home')
Including another URLconf:
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns: path('blog/', include('blog.urls'))
"""

from django.conf import \
    settings  # Import settings từ Django để truy cập cấu hình
from django.conf.urls.static import static  # Import để phục vụ các tệp tĩnh
from django.contrib import admin  # Import admin để quản lý admin site
from django.urls import path  # Import path để định nghĩa các đường dẫn URL
from drf_spectacular.views import (  # Import để tạo tài liệu API
    SpectacularAPIView, SpectacularSwaggerView)
from hotel.views import (BillViewSet,  # Import các view từ ứng dụng hotel
                         BookingManageViewSet, RoomViewSet,
                         StaffScheduleViewSet, StaffViewSet)
from rest_framework.routers import \
    DefaultRouter  # Import router từ Django REST Framework

router = DefaultRouter()  # Tạo một router để tự động tạo URL cho các viewsets

# Đăng ký các viewset với router để tạo ra các endpoint API
router.register("api/loki/room", RoomViewSet)  # Đăng ký RoomViewSet tại /api/loki/room
router.register("api/loki/staff", StaffViewSet)  # Đăng ký StaffViewSet tại /api/loki/staff
router.register("api/loki/schedule", StaffScheduleViewSet)  # Đăng ký StaffScheduleViewSet tại /api/loki/schedule
router.register("api/loki/booking", BookingManageViewSet)  # Đăng ký BookingManageViewSet tại /api/loki/booking
router.register("api/loki/bill", BillViewSet)  # Đăng ký BillViewSet tại /api/loki/bill

# Định nghĩa urlpatterns, bao gồm các đường dẫn cho admin và API documentation
urlpatterns = [
    path('admin/', admin.site.urls),  # Đường dẫn cho trang quản trị admin
    path('api/docs/schema/', SpectacularAPIView.as_view(), name='schema'),  # Đường dẫn cho schema API
    path('api/docs/schema/ui/', SpectacularSwaggerView.as_view()),  # Đường dẫn cho giao diện Swagger UI
] + router.urls  # Kết hợp các đường dẫn đã đăng ký trong router vào urlpatterns

# Nếu DEBUG mode đang bật, thêm các đường dẫn để phục vụ tệp phương tiện
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # Phục vụ tệp phương tiện

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from hotel.views import (BillViewSet, BookingManageViewSet, RoomViewSet,
                         StaffScheduleViewSet, StaffViewSet)
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

#router.register("api/room/select",RoomListViewSet) #/api/staff/select/?position_name=<position>
router.register("api/loki/room", RoomViewSet)
router.register("api/loki/staff", StaffViewSet )
router.register("api/loki/schedule", StaffScheduleViewSet)
router.register("api/loki/booking", BookingManageViewSet)
router.register("api/loki/bill", BillViewSet)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/docs/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/schema/ui/', SpectacularSwaggerView.as_view()),
   # path('api/room/select/<int:id>/', RoomListViewSet.as_view({'patch': 'patch'})),
] + router.urls

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)