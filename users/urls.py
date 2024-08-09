from django.urls import path, include
from .views import *
from . import views

urlpatterns = [
    path('users/', user_list, name='user_list'),
    path('update_user/', update_user, name='update_user'),
    path('delete_user/<int:user_id>/', delete_user, name='delete_user'),
    path('add_user/', add_user, name='add_user'),
    path('edit_user/<int:user_id>/', edit_user, name='edit_user'),
    path('profile/', profile_view, name='profile'),

]