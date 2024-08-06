from django.shortcuts import render,redirect,get_object_or_404,HttpResponse
from django.contrib.auth.decorators import login_required
from custom.models import *
from dnct.models import *
from django.contrib.auth.models import User, Group
from django.http import JsonResponse
from django.db.models import Count
from django.conf import settings


# Create your views here.
@login_required
def charts(request):
	data = {
	'title':"Charts"
	}
	return render(request,'charts.html',data)

@login_required
def chart_seksu_funcionariu(request):
	labels = []
	data = []
	queryset = Funcionariu.objects.values('sexo').annotate(total_seksu=Count('sexo'))
	for item in queryset:
		labels.append(item['sexo'])
		data.append(item['total_seksu'])
	return JsonResponse(data={
		'labels':labels,
		'data':data,
		})

@login_required
def chart_municipiu(request):
	labels = []
	data = []
	queryset = Funcionariu.objects.values('município__name').annotate(total_municipiu=Count('município__name'))
	for item in queryset:
		labels.append(item['município__name'])
		data.append(item['total_municipiu'])
	return JsonResponse(data={
		'labels':labels,
		'data':data,
		})

@login_required
def chart_estatuto_funcionariu(request):
    labels = []
    data = []
    queryset = Funcionariu.objects.values('estatuto').annotate(total_estatuto=Count('estatuto'))
    for item in queryset:
        estatuto_id = item['estatuto']
        estatuto_name = Status.objects.get(id=estatuto_id).name
        labels.append(estatuto_name)
        data.append(item['total_estatuto'])
    return JsonResponse(data={
        'labels': labels,
        'data': data,
    })

@login_required
def chart_depart_funcionariu(request):
    labels = []
    data = []
    queryset = Funcionariu.objects.values('direction').annotate(total_direction=Count('direction'))
    for item in queryset:
        direction_id = item['direction']
        direction_name = Department.objects.get(id=direction_id).name
        labels.append(direction_name)
        data.append(item['total_direction'])
    return JsonResponse(data={
        'labels': labels,
        'data': data,
    })

@login_required
def chart_statusonoff_funcionariu(request):
    labels = []
    data = []
    queryset = Funcionariu.objects.values('estatus_onoff').annotate(total_estatus_onoff=Count('estatus_onoff'))
    for item in queryset:
        estatus_onoff_id = item['estatus_onoff']
        estatus_onoff_name = Estatus.objects.get(id=estatus_onoff_id).estatus
        labels.append(estatus_onoff_name)
        data.append(item['total_estatus_onoff'])
    return JsonResponse(data={
        'labels': labels,
        'data': data,
    })
