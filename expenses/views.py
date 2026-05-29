from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
)

from django.contrib.auth.decorators import login_required

from .models import Category


@login_required
def category_list(request):

    categories = Category.objects.filter(
        user=request.user
    ).order_by('name')

    return render(
        request,
        'expenses/category_list.html',
        {
            'categories': categories
        }
    )


@login_required
def category_add(request):

    if request.method == 'POST':

        Category.objects.create(
            user=request.user,
            name=request.POST.get('name'),
            
        )

        return redirect('category_list')

    return render(
        request,
        'expenses/category_add.html'
    )


@login_required
def category_edit(request, pk):

    category = get_object_or_404(
        Category,
        pk=pk,
        user=request.user
    )

    if request.method == 'POST':

        category.name = request.POST.get('name')


        category.save()

        return redirect('category_list')

    return render(
        request,
        'expenses/category_edit.html',
        {
            'category': category
        }
    )


@login_required
def category_delete(request, pk):

    category = get_object_or_404(
        Category,
        pk=pk,
        user=request.user
    )

    category.delete()

    return redirect('category_list')