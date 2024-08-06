from django.shortcuts import render,redirect
from .models import *
from dnct.models import *
from custom.models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView

# Create your views here.
@login_required
def dashboard(request):
    context = {
        "title":"Dashboard",
        "active_varanda":"active",
    }
    return render(request,'main/dashboard.html',context)

@login_required
def dashboard(request):
    totfunc_mescc = Funcionariu.objects.count()
    permanente = Funcionariu.objects.filter(estatuto='1').count()
    AAP = Funcionariu.objects.filter(estatuto='2').count()
    kazuais = Funcionariu.objects.filter(estatuto='3').count()
    TC = Funcionariu.objects.filter(estatuto='4').count()
    AP = Funcionariu.objects.filter(estatuto='5').count()
    context = {
        'totfunc_mescc': totfunc_mescc,
        'permanente': permanente,
        'AAP': AAP,
        'kazuais': kazuais,
        'TC': TC,
        'AP': AP,

    }
    return render(request, 'main/dashboard.html', context)

@login_required
def estatuto_perm(request):
    funcionarios = Funcionariu.objects.filter(estatuto='1')
    context = {
        'funcionarios': funcionarios,
        'title': 'Funcionários Permanente'
    }
    return render(request, 'estatuto/estatuto_perm.html', context)

@login_required
def estatuto_aap(request):
    funcionarios = Funcionariu.objects.filter(estatuto='2')
    context = {
        'funcionarios': funcionarios,
        'title': 'Funcionários AAP'
    }
    return render(request, 'estatuto/estatuto_aap.html', context)

@login_required
def estatuto_kazuais(request):
    funcionarios = Funcionariu.objects.filter(estatuto='3')
    context = {
        'funcionarios': funcionarios,
        'title': 'Funcionários Casuais'
    }
    return render(request, 'estatuto/estatuto_kazuais.html', context)

@login_required
def estatuto_tc(request):
    funcionarios = Funcionariu.objects.filter(estatuto='4')
    context = {
        'funcionarios': funcionarios,
        'title': 'Funcionários Termo Certo'
    }
    return render(request, 'estatuto/estatuto_tc.html', context)

@login_required
def estatuto_ap(request):
    funcionarios = Funcionariu.objects.filter(estatuto='5')
    context = {
        'funcionarios': funcionarios,
        'title': 'Funcionários Apoiu Politico'
    }
    return render(request, 'estatuto/estatuto_ap.html', context)


class MyPasswordChangeView(PasswordChangeView):
    template_name = 'main/change_password.html'
    success_url = reverse_lazy('password_change_done')

class MyPasswordChangeDoneView(PasswordChangeDoneView):
    template_name = 'main/password_change_done.html'

def custom_logout(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login')  # Redirect to the login page after logging out
    else:
        # You might want to handle GET requests differently or show a confirmation page
        return redirect('login')
