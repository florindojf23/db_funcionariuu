from django.urls import path
from django.contrib.auth import views as auth_views
from .views import *
from . import views
from django.conf.urls.static import static

urlpatterns=[
    path('charts/', charts, name="charts"),
	path('chart_seksu_funcionariu/', chart_seksu_funcionariu, name="chart_seksu_funcionariu"),
	path('chart_municipiu/', chart_municipiu, name="chart_municipiu"),
	path('chart_estatuto_funcionariu/', chart_estatuto_funcionariu, name="chart_estatuto_funcionariu"),
	path('chart_depart_funcionariu/', chart_depart_funcionariu, name="chart_depart_funcionariu"),
	path('chart_statusonoff_funcionariu/', chart_statusonoff_funcionariu, name="chart_statusonoff_funcionariu"),
	
]
