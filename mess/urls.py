from django.urls import path
from . import views

urlpatterns = [
    # path('', views.api_mess_list, name='api_mess_list'),
    path('create/', views.api_mess_create, name='api_mess_create'),
    path('update/<int:mess_id>/', views.api_mess_update, name='api_mess_update'),
    path('delete/<int:mess_id>/', views.api_mess_delete, name='api_mess_delete'),
    path('<int:mess_id>/', views.api_mess_detail, name='api_mess_detail'),

    # path('menu/', views.api_mess_menu, name='api_mess_menu'),
    # path('menu/create/', views.api_mess_menu_create, name='api_mess_menu_create'),
    # path('menu/update/', views.api_mess_menu_update, name='api_mess_menu_update'),
]
