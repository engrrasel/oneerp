from django.urls import path
from . import views

urlpatterns = [

    path(
        '',
        views.transaction_list,
        name='transaction_list'
    ),

    path(
        'add/',
        views.transaction_add,
        name='transaction_add'
    ),

    path(
        '<int:pk>/edit/',
        views.transaction_edit,
        name='transaction_edit'
    ),

    path(
        '<int:pk>/delete/',
        views.transaction_delete,
        name='transaction_delete'
    ),

    path(
        'deleted/',
        views.deleted_transactions,
        name='deleted_transactions'
    ),

    path(
        '<int:pk>/restore/',
        views.transaction_restore,
        name='transaction_restore'
    ),


    path(
        '<int:pk>/history/',
        views.transaction_history,
        name='transaction_history'
    ),
]