from django.urls import path
from . import views

urlpatterns = [
    path('', views.api_resource_list, name='resource_list'),
    path('search/', views.api_resource_search, name='resource_search'),
    path('create/', views.api_resource_create, name='resource_create'),
    path('update/<str:resource_id>/', views.api_resource_update, name='resource_update'),
    path('delete/<str:resource_id>/', views.api_resource_delete, name='resource_delete'),
    path('<str:resource_id>/', views.api_resource_detail, name='resource_detail'),
]
