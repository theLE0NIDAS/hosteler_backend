from django.urls import path
from . import views

urlpatterns = [
    # API views
    path('list/', views.api_complaint_list, name='api_complaint_list'),
    path('mycomplaint/<str:student_id>/', views.api_mycomplaint, name='api_mycomplaint'),
    path('search/', views.api_complaint_search, name='api_complaint_search'),
    path('create/', views.api_complaint_create, name='api_complaint_create'),
    path('update/<str:complaint_id>/', views.api_complaint_update, name='api_complaint_update'),
    path('delete/<str:complaint_id>/', views.api_complaint_delete, name='api_complaint_delete'),
]
