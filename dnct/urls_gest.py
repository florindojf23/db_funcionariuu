from django.urls import path
from dnct.views_gest import *
from . import views_gest

urlpatterns=[
	path('g_funcionariu',g_funcionariu, name='g_funcionariu'),
    path('g_detail_funcionariu/<str:pk>', g_detailFuncionariu,  name = 'g_detail_funcionariu'),
	path('csv_funcionariu/', csv_funcionariu, name="csv_funcionariu"),
	path('pdf_funcionariu/', pdf_funcionariu, name="pdf_funcionariu"),

	path('g_leave',g_leave, name='g_leave'),
	path('detail_leave/<str:pk>', detailLeave,  name = 'detail_leave'),
    path('csv_leave/', csv_leave, name="csv_leave"),
	path('pdf_leave/', pdf_leave, name="pdf_leave"),
    path('archive/<int:leave_id>/', archive_leave, name='archive_leave'),
    path('g_history/', g_history_leave, name='g_history_leave'),
    path('list/', leave_list, name='leave_list'),

]
