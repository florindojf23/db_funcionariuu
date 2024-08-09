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
from .models import *
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

# Create your views here.
@login_required
def funcionariu(request):
    listafuncionariu = Funcionariu.objects.all()
    data = {
    'title':"Lista dos Funcionários",
    'active_estudante':"active",
    'dadus':listafuncionariu
    }
    return render(request, 'admin/listafuncionariu.html',data)

@login_required
def createFuncionariu(request):
    tinan = Tinan.objects.all().order_by('-id')
    form = FuncionariuForm()

    if request.method == 'POST':
        form = FuncionariuForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Dados Está Adicionados!')
            return redirect('funcionariu')
    data = {
        'form':form,
        'listaTinan':tinan,
        'title':"Formuláriu do Novo Funcionário",
        'page':"form",
    }
    return render(request, 'admin/formfuncionariu.html',data)

@login_required
def updateDetailFuncionariu(request, id):
    tinan = Tinan.objects.all().order_by('-id')
    funcionariu = get_object_or_404(Funcionariu, id=id)
    form = FuncionariuForm(instance=funcionariu)

    if request.method == 'POST':
        form = FuncionariuForm(request.POST, request.FILES, instance=funcionariu)
        if form.is_valid():
            form.save()
            messages.success(request, 'Dados Está Atualizado!')
            return redirect('funcionariu')
    data = {
        'form': form,
        'tinan': tinan,
        'title': "Formulário de Atualização de Funcionário",
        'page': "form",
    }
    return render(request, 'admin/formfuncionariu.html', data)


@login_required
def deleteFuncionariu(request,pk):
    funcionariu = Funcionariu.objects.get(id=pk)
    funcionariu.delete()
    messages.success(request, 'Dados Estão Apagados!')
    return redirect('funcionariu')

@login_required
def detailFuncionariu(request,pk):
    funcionariuData = get_object_or_404(Funcionariu,id=pk)
    data = {
    'title':"Detalho do Funcionário",
    'funcionariuData':funcionariuData,
    'page':"view",
    'active_estudante':"active",
    }
    return render(request, 'admin/formfuncionariu.html',data)

# @login_required
# def csv_funcionariu(request):
#     # replace with the fields you need 
#     fields = ['nu_id','nome_completo','sexo','naturalidade','data_do_nasc','data_entrada','validade','direction__name','posição','endereço','município__name','estatuto','estatus_onoff','nu_contacto','email']
#     # Generate the csv file with datetime
#     response = HttpResponse(content_type="text/csv")
#     response["Content-Disposition"] = f"attachment; filename=listafuncionariuGeral.csv"
#     writer = csv.writer(response)
#     # Write the header row
#     writer.writerow(fields)
#     # Use the fields to get the data, specifying the model name
#     for row in Funcionariu.objects.values(*fields):
#         writer.writerow([row[field] for field in fields])
#         # return
#     return response

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
def upload_csv(request):
    if request.method == 'POST':
        form = UploadCSVForm(request.POST, request.FILES)
        if form.is_valid():
            csvfile = request.FILES['csv_file']
            
            # Detect file encoding
            raw_data = csvfile.read()
            result = chardet.detect(raw_data)
            encoding = result['encoding']
            
            # Decode file content
            decoded_file = raw_data.decode(encoding).splitlines()
            reader = csv.reader(decoded_file, delimiter=';')

            # Skip the header row
            next(reader)

            errors = []

            for row in reader:
                # Ensure the row has enough columns
                if len(row) < 15:
                    errors.append(f"Skipping row (not enough columns): {row}")
                    continue

                try:
                    # Check if a Funcionariu with the same `nu_id` already exists
                    if Funcionariu.objects.filter(nu_id=row[0]).exists():
                        errors.append(f"Skipping duplicate row with nu_id: {row[0]}")
                        continue

                    # Fetch related instances
                    direction = Department.objects.get(sigla=row[7])
                    municipio = Municipality.objects.get(name=row[10])
                    estatuto = Status.objects.get(name=row[11])
                    estatus_onoff = Estatus.objects.get(estatus=row[12])

                    # Create a new Funcionariu object
                    new_funcionariu = Funcionariu.objects.create(
                        nu_id=row[0],
                        nome_completo=row[1],
                        sexo=row[2],
                        naturalidade=row[3],
                        data_do_nasc=row[4],
                        data_entrada=row[5],
                        validade=row[6],
                        direction=direction,
                        posição=row[8],
                        endereço=row[9],
                        município=municipio,
                        estatuto=estatuto,
                        estatus_onoff=estatus_onoff,
                        nu_contacto=row[13],
                        email=row[14]
                        # Uncomment and handle these fields if necessary
                        # fotografia=row[14] if row[14] else None,
                        # documentos=row[15] if row[15] else None
                    )
                    print(f"Created Funcionariu: {new_funcionariu}")
                except Department.DoesNotExist:
                    errors.append(f"Department not found: {row[7]}")
                except Municipality.DoesNotExist:
                    errors.append(f"Municipality not found: {row[10]}")
                except Status.DoesNotExist:
                    errors.append(f"Status not found: {row[11]}")
                except Estatus.DoesNotExist:
                    errors.append(f"Estatus not found: {row[12]}")
                except IntegrityError as e:
                    errors.append(f"IntegrityError: {e}")
                except Exception as e:
                    errors.append(f"Error creating Funcionariu: {e}")
            
            if errors:
                print("Errors occurred:")
                for error in errors:
                    print(error)
                # Optionally, display errors on the webpage
                messages.error(request, "Errors occurred during CSV import. Check console for details.")

            return render(request, 'admin/success.html')
        else:
            print(f"Form is not valid: {form.errors}")
    else:
        form = UploadCSVForm()
    return render(request, 'admin/upload_csv.html', {'form': form})

def upload_success(request):
    return render(request, 'admin/success.html')

# def upload_csv(request):
#     if request.method == 'POST':
#         form = UploadCSVForm(request.POST, request.FILES)
#         if form.is_valid():
#             csvfile = request.FILES['csv_file']
#             decoded_file = csvfile.read().decode('utf-8').splitlines()
#             reader = csv.reader(decoded_file,delimiter=';')

#             # Skip the header row
#             next(reader)

#             errors = []

#             for row in reader:
#                 # Ensure the row has enough columns
#                 if len(row) < 14:
#                     errors.append(f"Skipping row (not enough columns): {row}")
#                     continue

#                 try:
#                      # Check if a Funcionariu with the same `nu` already exists
#                     if Funcionariu.objects.filter(nu=row[0]).exists():
#                         errors.append(f"Skipping duplicate row with nu: {row[0]}")
#                         continue

#                     # Create a new Funcionariu object
#                     new_funcionariu = Funcionariu.objects.create(
#                         nu_id=row[0],
#                         nome_completo=row[1],
#                         sexo=row[2],
#                         naturalidade=row[3],
#                         data_do_nasc=row[4],
#                         data_entrada=row[5],
#                         validade=row[6],
#                         posição=row[7],
#                         direção=row[8],
#                         endereço=row[9],
#                         município=row[10],
#                         estatuto_id=row[11],
#                         nu_contacto=row[12],
#                         email=row[13]
#                         # Uncomment and handle these fields if necessary
#                         # fotografia=row[14] if row[14] else None,
#                         # documentos=row[15] if row[15] else None
#                     )
#                     print(f"Created Funcionariu: {new_funcionariu}")
#                 except IntegrityError as e:
#                     print(f"IntegrityError: {e}")
#                 except Exception as e:
#                     print(f"Error creating Funcionariu: {e}")
            
#             return render(request, 'success.html')
#         else:
#             print(f"Form is not valid: {form.errors}")
#     else:
#         form = UploadCSVForm()
#     return render(request, 'upload_csv.html', {'form': form})

# def upload_success(request):
#     return render(request, 'success.html')

def birthday_notifications(request):
    print("Birthday notification view called")
    today = date.today()
    employees = Funcionariu.objects.filter(data_do_nasc__month=today.month, data_do_nasc__day=today.day)
    return render(request, 'notification/halo_tinan.html', {'employees': employees})

def birthday_count(request):
    today = date.today()
    birthday_count = Funcionariu.objects.filter(data_do_nasc__month=today.month, data_do_nasc__day=today.day).count()
    return JsonResponse({'count': birthday_count})

