from django.urls import path
from dnct.views_leaves import *
from . import views_leaves

urlpatterns=[
    path('leave/', views_leaves.leave, name='leave'),
    path('create_leave', createLeave, name='create_leave'),
	path('update_leave/<str:id>', updateLeave, name='update_leave'),
	path('delete_leave/<str:pk>', deleteLeave, name='delete_leave'),
	path('detail_leave/<str:pk>', detailLeave,  name = 'detail_leave'),
    path('csv_leave/', csv_leave, name="csv_leave"),
	path('pdf_leave/', pdf_leave, name="pdf_leave"),

    path('leave/archive/<int:leave_id>/', views_leaves.archive_leave, name='archive_leave'),
    path('archive/<int:leave_id>/', archive_leave, name='archive_leave'),
    path('history/', history_leave, name='history_leave'),
    path('list/', leave_list, name='leave_list'),
    path('bulk-delete-leave/', bulk_delete_leave, name='bulk_delete_leave'),

]
