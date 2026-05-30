from django.urls import path
from . import views

urlpatterns = [
    path('', views.wallet_list, name='wallet_list'),
    path('add/', views.wallet_add, name='wallet_add'),
    path('edit/<int:pk>/', views.wallet_edit, name='wallet_edit'),
    path('delete/<int:pk>/', views.wallet_delete, name='wallet_delete'),


    path(
    '<int:pk>/',
    views.wallet_detail,
    name='wallet_detail'
),

    path(
        'add/',
        views.transfer_add,
        name='transfer_add'
    ),

    path(
    'transfers/add/',
    views.transfer_add,
    name='transfer_add'
),

path(
    'wallets/<int:pk>/restore/',
    views.wallet_restore,
    name='wallet_restore'
),


]