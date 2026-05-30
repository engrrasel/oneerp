from django.urls import path

from . import views


urlpatterns = [

    path(
        '',
        views.profile_detail,
        name='profile'
    ),

    path(
        'edit/',
        views.profile_edit,
        name='profile_edit'
    ),

        path(
        'settings/',
        views.settings_view,
        name='settings'
    ),

]