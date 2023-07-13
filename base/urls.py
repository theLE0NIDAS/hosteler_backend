from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/login/', views.api_admin_login, name='api_admin_login'),
    path('student/login/', views.api_student_login, name='api_student_login'),
    path('logout/', views.api_logout, name='api_logout'),

    path('admin/register/', views.api_admin_create, name='api_admin_create'),
    path('admin/update/<str:username>/', views.api_admin_update_password, name='api_admin_update_password'),
    path('student/update/<str:roll_number>/', views.api_student_update_password, name='api_student_update_password'),

    path('student/', include('student.urls')),
    path('attendance/', include('attendance.urls')),
    path('resource/', include('resource.urls')),
    path('room/', include('room.urls')),
    path('mess/', include('mess.urls')),
    path('complaint/', include('complaint.urls')),
]
