from django.urls import path
from . import views

urlpatterns = [
    # API views

    path('leave/', views.api_leave_list, name='api_leave_list'),
    # path('leave/<int:leave_id>/', views.api_leave_detail, name='api_leave_detail'),
    path('leave/create/', views.api_leave_create, name='api_leave_create'),
    path('leave/myleave/<str:roll_number>/', views.api_myleave, name='api_myleave'),
    path('leave/update/<int:leave_id>/', views.api_leave_update, name='api_leave_update'),
    path('leave/delete/<int:leave_id>/', views.api_leave_delete, name='api_leave_delete'),

    path('rebate/', views.api_rebate_list, name='api_rebate_list'),
    path('rebate_amount/<str:roll_number>/', views.api_total_rebate_amount, name='api_total_rebate_amount'),
    # path('rebate/<int:rebate_id>/', views.api_rebate_detail, name='api_rebate_detail'),
    path('rebate/create/', views.api_rebate_create, name='api_rebate_create'),
    # path('rebate/<int:rebate_id>/update/', views.api_rebate_update, name='api_rebate_update'),
    # path('rebate/<int:rebate_id>/delete/', views.api_rebate_delete, name='api_rebate_delete'),
    
    path('', views.api_attendance_list, name='api_attendance_list'),
    path('search/', views.api_attendance_search, name='api_attendance_search'),
    path('create/', views.api_attendance_create, name='api_attendance_create'),
    path('update/<str:roll_number>/', views.api_attendance_update, name='api_attendance_update'),
    path('<str:roll_number>/', views.api_attendance_detail, name='api_attendance_detail'),
    # path('<int:attendance_id>/delete/', views.api_attendance_delete, name='api_attendance_delete'),
]
