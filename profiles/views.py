from django.shortcuts import (
    render,
    redirect
)

from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Profile


@login_required
def profile_detail(request):

    profile = request.user.profile

    return render(
        request,
        'profiles/profile_detail.html',
        {
            'profile': profile
        }
    )


@login_required
def profile_edit(request):

    profile = request.user.profile

    if request.method == 'POST':

        profile.full_name = request.POST.get(
            'full_name',
            ''
        )

        profile.phone = request.POST.get(
            'phone',
            ''
        )

        profile.address = request.POST.get(
            'address',
            ''
        )

        profile.city = request.POST.get(
            'city',
            ''
        )

        profile.country = request.POST.get(
            'country',
            ''
        )

        if request.FILES.get(
            'profile_photo'
        ):

            profile.profile_photo = (
                request.FILES.get(
                    'profile_photo'
                )
            )

        profile.save()

        messages.success(
            request,
            'Profile updated successfully.'
        )

        return redirect(
            'profile'
        )

    return render(
        request,
        'profiles/profile_edit.html',
        {
            'profile': profile
        }
    )