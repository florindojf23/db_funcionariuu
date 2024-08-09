from django.urls import path
from .views import *

urlpatterns=[
	path('funcionariu',funcionariu, name='funcionariu'),
	path('create_funcionariu', createFuncionariu, name='create_funcionariu'),
	path('delete_funcionariu/<str:pk>', deleteFuncionariu, name='delete_funcionariu'),
	path('detail_funcionariu/<str:pk>', detailFuncionariu,  name = 'detail_funcionariu'),
	path('csv_funcionariu/', csv_funcionariu, name="csv_funcionariu"),
	path('pdf_funcionariu/', pdf_funcionariu, name="pdf_funcionariu"),
	path('upload_csv/', upload_csv, name='upload_csv'),
    path('upload_success/', upload_success, name='upload_success'),
    path('update_detail_funcionariu/<str:id>/', updateDetailFuncionariu, name='update_detail_funcionariu'),
    path('birthday-notifications/', birthday_notifications, name='birthday_notifications'),
	path('birthday-count/', birthday_count, name='birthday_count'),
	# path('search/', search_view, name='search'),
	
]
