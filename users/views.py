from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .forms import *

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

def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.delete()
    return redirect('user_list')

def add_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user_list')
    else:
        form = UserCreationForm()
    return render(request, 'add_edit_user.html', {'form': form, 'title': 'Add User'})

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