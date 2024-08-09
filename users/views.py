from django.shortcuts import render, get_object_or_404, redirect,HttpResponse
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .forms import *
from django.contrib.auth.decorators import login_required
from .models import *
from dnct.models import *
from custom.models import *
from django.urls import reverse_lazy
from django.contrib.auth import logout

@login_required
def user_list(request):
    users = User.objects.all()
    context = {
        'userlist': users
    }
    return render(request, 'user_list.html', context)

@csrf_exempt
def update_user(request):
    if request.method == "POST":
        user_id = request.POST.get('id')
        field = request.POST.get('type')
        value = request.POST.get('value')

        user = get_object_or_404(User, id=user_id)
        setattr(user, field, value)
        user.save()

        return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'error'})


@login_required
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.delete()
    return redirect('user_list')


@login_required
def add_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user_list')
    else:
        form = UserCreationForm()
    return render(request, 'add_edit_user.html', {'form': form, 'title': 'Add User'})


@login_required
def edit_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = UserChangeForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user_list')
    else:
        form = UserChangeForm(instance=user)
    return render(request, 'add_edit_user.html', {'form': form, 'title': 'Edit User'})


@login_required
def profile_view(request):
    return render(request, 'profile.html', {'user': request.user})


# @login_required
# def profile_update(request, username):
#     user = get_object_or_404(User, username=username)
#     if request.method == 'POST':
#         user_form = UserUpdateForm(request.POST, instance=user)
#         profile_form = UserProfileForm(request.POST, request.FILES, instance=user.userprofile)
#         if user_form.is_valid() and profile_form.is_valid():
#             user_form.save()
#             profile_form.save()
#             return redirect('users:profile', username=username)
#     else:
#         user_form = UserUpdateForm(instance=user)
#         profile_form = UserProfileForm(instance=user.userprofile)
    
#     return render(request, 'profile_update.html', {'user_form': user_form, 'profile_form': profile_form, 'user': user})


