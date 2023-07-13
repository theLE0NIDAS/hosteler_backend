from django.urls import path
from . import views

urlpatterns = [
    path('', views.api_room_list, name='room_list'),
    path('search/', views.api_room_search, name='room_search'),
    path('create/', views.api_room_create_floor, name='room_create_floor'),
    path('register/<int:room_number>/', views.api_room_student_register, name='room_student_register'),
    path('deregister/<int:room_number>/', views.api_room_student_deregister, name='room_student_deregister'),
    # path('update/<int:room_id>/', views.api_room_update, name='room_update'),
    path('delete/<int:room_number>/', views.api_room_delete, name='room_delete'),
    path('<int:room_number>/', views.api_room_detail, name='room_detail'),
]
