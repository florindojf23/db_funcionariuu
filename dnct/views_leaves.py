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
def leave(request):
    listalicensafuncionariu = Leave.objects.all()
    data = {
    'title':"Lista de Licenças dos Funcionários",
    'active_estudante':"active",
    'dadus':listalicensafuncionariu
    }
    return render(request, 'leaves/listaleaves.html',data)

@login_required
def createLeave(request):
    tinan = Tinan.objects.all().order_by('-id')
    form = LeavesForm()

    if request.method == 'POST':
        form = LeavesForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Dados Está Adicionados!')
            return redirect('leave')
    data = {
        'form':form,
        'listaTinan':tinan,
        'title':"Formulário de Licença de Funcionário",
        'page':"form",
    }
    return render(request, 'leaves/formleaves.html',data)

@login_required
def updateLeave(request, id):
    tinan = Tinan.objects.all().order_by('-id')
    leave = Leave.objects.get(id=id)
    form = LeavesForm(instance=leave)

    if request.method == 'POST':
        form = LeavesForm(request.POST, request.FILES, instance=leave)
        if form.is_valid():
            form.save()
            messages.success(request, 'Dados Está Atualizado!')
            return redirect('leave')
    data = {
        'form': form,
        'tinan': tinan,
        'title': "Formulário de Atualização da Licença de Funcionário",
        'page': "form",
    }
    return render(request, 'leaves/formleaves.html', data)

@login_required
def deleteLeave(request,pk):
    leave = Leave.objects.get(id=pk)
    leave.delete()
    messages.success(request, 'Dados Estão Apagados!')
    return redirect('leave')

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
    return render(request, 'leaves/formleaves.html', data)

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
    return render(request, 'leaves/list_leaves.html', {'leaves': leaves, 'title': 'Leave List'})

@login_required
def history_leave(request):
    archived_leaves = Leave.objects.filter(archived=True)
    return render(request, 'leaves/history_leave.html', {'archived_leaves': archived_leaves, 'title': 'Archived Leave History'})

@login_required
def bulk_delete_leave(request):
    if request.method == 'POST':
        leave_ids = request.POST.getlist('leaves_to_delete')
        Leave.objects.filter(id__in=leave_ids).delete()
        messages.success(request, 'Licenças selecionadas excluídas com sucesso!')
    return redirect('leave')