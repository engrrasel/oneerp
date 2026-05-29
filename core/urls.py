from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [

    path(
        'admin/',
        admin.site.urls
    ),

    path(
        '',
        include(
            'user_accounts.urls'
        )
    ),

    path(
        '',
        include(
            'expenses.urls'
        )
    ),

    path(
        'transactions/',
        include(
            'transactions.urls'
        )
    ),

    path(
        'dashboard/',
        include(
            'dashboard.urls'
        )
    ),

    path(
        'wallets/',
        include(
            'wallets.urls'
        )
    ),

    path(
        'profile/',
        include(
            'profiles.urls'
        )
    ),

]


if settings.DEBUG:

    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )