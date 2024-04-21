from django.urls import path
from django.contrib import admin
from .views import register, login, generate_qr_code, get_qr_code_details, get_user_qr_codes, update_qr_code, delete_qr_code, get_all_users, update_user, delete_user

urlpatterns = [
    path('api/auth/register/', register, name='register'),
    path('api/auth/login/', login, name='login'),
    path('api/qrcodes/', generate_qr_code, name='generate_qr_code'),
    path('api/qrcodes/<int:pk>/', get_qr_code_details, name='get_qr_code_details'),
    path('api/user/qrcodes/', get_user_qr_codes, name='get_user_qr_codes'),
    path('api/qrcodes/update/<int:pk>/', update_qr_code, name='update_qr_code'),
    path('api/qrcodes/delete/<int:pk>/', delete_qr_code, name='delete_qr_code'),
    path('api/users/', get_all_users, name='get_all_users'),
    path('api/users/update/<int:pk>/', update_user, name='update_user'),
    path('api/users/delete/<int:pk>/', delete_user, name='delete_user'),
    path('admin/', admin.site.urls),
    
]

