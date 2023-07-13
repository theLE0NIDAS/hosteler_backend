from django.urls import path
from . import views

urlpatterns = [
    # API views
    path('', views.api_student_list, name='api_student_list'),
    path('search/', views.api_student_search, name='api_student_search'),
    path('create/', views.api_student_create, name='api_student_create'),
    path('update/<str:roll_number>/', views.api_student_update, name='api_student_update'),
    path('delete/<str:roll_number>/', views.api_student_delete, name='api_student_delete'),
    path('<str:roll_number>/', views.api_student_detail, name='api_student_detail'),
]
