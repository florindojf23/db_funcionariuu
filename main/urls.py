from django.urls import path
from django.contrib.auth import views as auth_views
from .views import *

urlpatterns = [
	path('', dashboard, name="home"),
	path('dashboard',dashboard, name='dashboard'),
    path('estatuto/perm/', estatuto_perm, name='estatuto_perm'),
    path('estatuto/aap/', estatuto_aap, name='estatuto_aap'),
    path('estatuto/casuais/', estatuto_kazuais, name='estatuto_kazuais'),
    path('estatuto/tc/', estatuto_tc, name='estatuto_tc'),
    path('estatuto/ap/', estatuto_ap, name='estatuto_ap'),
	path('change-password/', MyPasswordChangeView.as_view(), name='change_password'),
    path('password-change-done/', MyPasswordChangeDoneView.as_view(), name='password_change_done'),
    path('logout/', custom_logout, name='logout'),
]