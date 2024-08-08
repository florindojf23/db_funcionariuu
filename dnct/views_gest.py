from django.shortcuts import render,redirect,get_object_or_404,HttpResponse
from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.contrib.auth.hashers import make_password
from custom.models import *
from custom.utils import *
from dnct.models import *
from .forms import *
import os
import csv
import datetime
import chardet
import logging
from django.db import IntegrityError
from .forms import UploadCSVForm
from django.conf import settings

#pdf lib
from io import BytesIO
from django.template.loader import get_template
from xhtml2pdf import pisa

@login_required
def g_funcionariu(request):
    listafuncionariu = Funcionariu.objects.all()
    data = {
    'title':"Lista dos Funcionários",
    'active_estudante':"active",
    'dadus':listafuncionariu
    }
    return render(request, 'gestor/listafuncionariu.html',data)

@login_required
def g_detailFuncionariu(request,pk):
    funcionariuData = get_object_or_404(Funcionariu,id=pk)
    data = {
    'title':"Detalho do Funcionário",
    'funcionariuData':funcionariuData,
    'page':"view",
    'active_estudante':"active",
    }
    return render(request, 'gestor/formfuncionariu.html',data)

@login_required
def csv_funcionariu(request):
    # Define the fields and headers for the CSV file
    fields = {
        'nu_id': 'ID',
        'nome_completo': 'Name',
        'sexo': 'Sex',
        'naturalidade': 'Naturalidade',
        'data_do_nasc': 'Date of Birth',
        'data_entrada': 'Date of Entry',
        'validade': 'Validity',
        'direction__name': 'Direction',
        'posição': 'Position',
        'endereço': 'Address',
        'município__name': 'Municipality',
        'estatuto__name': 'Status',
        'estatus_onoff__estatus': 'Status On/Off',
        'nu_contacto': 'Contact Number',
        'email': 'Email'
    }

    # Generate the CSV file
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = "attachment; filename=listafuncionariuGeral.csv"
    writer = csv.writer(response)

    # Write the header row with custom names
    writer.writerow(fields.values())

    # Retrieve data including related names
    data = Funcionariu.objects.select_related(
        'direction', 
        'município', 
        'estatuto', 
        'estatus_onoff'
    ).all()

    # Write data rows with related field names
    for funcionario in data:
        writer.writerow([
            funcionario.nu_id,
            funcionario.nome_completo,
            funcionario.sexo,
            funcionario.naturalidade,
            funcionario.data_do_nasc,
            funcionario.data_entrada,
            funcionario.validade,
            funcionario.direction.name if funcionario.direction else '',
            funcionario.posição,
            funcionario.endereço,
            funcionario.município.name if funcionario.município else '',
            funcionario.estatuto.name if funcionario.estatuto else '',
            funcionario.estatus_onoff.estatus if funcionario.estatus_onoff else '',
            funcionario.nu_contacto,
            funcionario.email
        ])

    return response

@login_required
def pdf_funcionariu(request):
    funcionariu = Funcionariu.objects.all()
    data = {'dadus':funcionariu,
            'title':"PDF Docs"}
    pdf = render_to_pdf('pdf/funcionariupdf.html',data)
    return HttpResponse(pdf,content_type='application/pdf')

def render_to_pdf(template_src,context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")),result)
    if not pdf.err:
        return HttpResponse(result.getvalue(),content_type='application/pdf')
    return None

@login_required
def g_leave(request):
    listalicensafuncionariu = Leave.objects.all()
    data = {
    'title':"Lista de Licenças dos Funcionários",
    'active_estudante':"active",
    'dadus':listalicensafuncionariu
    }
    return render(request, 'gestor/listaleaves.html',data)


@login_required
def detailLeave(request, pk):
    leaveData = get_object_or_404(Leave, id=pk)
    leave_days = leaveData.calculate_leave_days()
    data = {
        'title': "Detalho da Licença de Funcionário",
        'leaveData': leaveData,
        'leave_days': leave_days,
        'page': "view",
        'active_estudante': "active",
    }
    return render(request, 'gestor/formleaves.html', data)

@login_required
def csv_leave(request):
    # replace with the fields you need 
    fields = ['employee__nome_completo','leave_type','start_date','end_date','status','reason']
    # Generate the csv file with datetime
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = f"attachment; filename=listalicensadosfuncionarios.csv"
    writer = csv.writer(response)
    # Write the header row
    writer.writerow(fields)
    # Use the fields to get the data, specifying the model name
    for row in Leave.objects.values(*fields):
        writer.writerow([row[field] for field in fields])
        # return
    return response

@login_required
def pdf_leave(request):
    leave = Leave.objects.all()
    data = {'dadus':leave,
            'title':"PDF Docs"}
    pdf = render_to_pdf('pdf/leavepdf.html',data)
    return HttpResponse(pdf,content_type='application/pdf')

def render_to_pdf(template_src,context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")),result)
    if not pdf.err:
        return HttpResponse(result.getvalue(),content_type='application/pdf')
    return None

@login_required
def archive_leave(request, leave_id):
    leave = get_object_or_404(Leave, id=leave_id)
    leave.archived = True
    leave.save()
    messages.success(request, 'Licença arquivada com sucesso!')
    return redirect('leave_list')

@login_required
def leave_list(request):
    leaves = Leave.objects.filter(archived=False)
    return render(request, 'gestor/list_leaves.html', {'leaves': leaves, 'title': 'Leave List'})

@login_required
def g_history_leave(request):
    archived_leaves = Leave.objects.filter(archived=True)
    return render(request, 'gestor/history_leave.html', {'archived_leaves': archived_leaves, 'title': 'Archived Leave History'})