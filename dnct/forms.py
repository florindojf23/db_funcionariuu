from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Button, HTML
from django.contrib.auth.models import Group,User
from django.forms.widgets import FileInput
from django.db.models import Q
from .models import *
from custom.models import *

class UploadCSVForm(forms.Form):
    csv_file = forms.FileField()

class UploadFileForm(forms.Form):
    file = forms.FileField()

class DateInput(forms.DateInput):
    input_type = 'date'

class FuncionariuForm(forms.ModelForm):
    data_do_nasc = forms.DateField(label='Data Moris', widget=DateInput())
    data_entrada = forms.DateField(label='Data Entrada', widget=DateInput())
    validade = forms.DateField(label='Data Remata', widget=DateInput())
    
    class Meta:
        model = Funcionariu
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Update labels for each field
        self.fields['nu_id'].label = 'No Id'
        self.fields['nome_completo'].label = 'Nome Completo'
        self.fields['sexo'].label = 'Sexo'
        self.fields['naturalidade'].label = 'Naturalidade'
        self.fields['data_do_nasc'].label = 'Data do Nasc.'
        self.fields['data_entrada'].label = 'Data de Início'
        self.fields['validade'].label = 'Data de Término'
        self.fields['posição'].label = 'Posição'
        self.fields['direction'].label = 'Direção/Unidade'
        self.fields['endereço'].label = 'Endereço'
        self.fields['município'].label = 'Município'
        self.fields['estatuto'].label = 'Tipo de Contrato'
        self.fields['estatus_onoff'].label = 'Status'
        self.fields['nu_contacto'].label = 'No Contacto'
        self.fields['email'].label = 'Email'
        self.fields['fotografia'].label = 'Fotografia'
        self.fields['documentos'].label = 'Documentos'

        
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('nu_id', css_class='form-group col-md-3 mb-0'),
                Column('nome_completo', css_class='form-group col-md-6 mb-0'),
                Column('sexo', css_class='form-group col-md-3 mb-0'),
            ),
            Row(
                Column('naturalidade', css_class='form-group col-md-3 mb-0'),
                Column('data_do_nasc', css_class='form-group col-md-6 mb-0'),
                Column('data_entrada', css_class='form-group col-md-3 mb-0'),
            ),
            Row(
                Column('validade', css_class='form-group col-md-3 mb-0'),
                Column('posição', css_class='form-group col-md-6 mb-0'),
                Column('direction', css_class='form-group col-md-3 mb-0'),
            ),
            Row(
                Column('endereço', css_class='form-group col-md-3 mb-0'),
                Column('município', css_class='form-group col-md-6 mb-0'),
                Column('estatuto', css_class='form-group col-md-3 mb-0'),
            ),
            Row(
                Column('nu_contacto', css_class='form-group col-md-3 mb-0'),
                Column('email', css_class='form-group col-md-6 mb-0'),
                Column('estatus_onoff', css_class='form-group col-md-3 mb-0'),

            ),
            Row(
                Column('fotografia', css_class='form-group col-md-6 mb-0'),
                Column('documentos', css_class='form-group col-md-6 mb-0'),

            ),
            HTML(""" <div class="text-left mt-4"> <button class="btn btn-sm btn-labeled btn-info" type="submit" title="Update"><span class="btn-label"><i class='fa fa-save'></i></span> Save</button>"""),
            HTML("""  <button class="btn btn-sm btn-labeled btn-secondary" onclick=self.history.back()><span class="btn-label"><i class="fa fa-window-close"></i></span> Cancel</button></div>""")
        )
        

class LeavesForm(forms.ModelForm):
    start_date = forms.DateField(label='Data Entrada', widget=DateInput())
    end_date = forms.DateField(label='Data Remata', widget=DateInput())
    
    class Meta:
        model = Leave
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Update labels for each field
        self.fields['employee'].label = 'Funcionário'
        self.fields['leave_type'].label = 'Tipo de Licença'
        self.fields['start_date'].label = 'Data de Início'
        self.fields['end_date'].label = 'Data de Término'
        self.fields['reason'].label = 'Motivo'
        # self.fields['status'].label = 'Status'

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('employee', css_class='form-group col-md-6 mb-0'),
                Column('leave_type', css_class='form-group col-md-6 mb-0'),
            ),
            Row(
                Column('start_date', css_class='form-group col-md-6 mb-0'),
                Column('end_date', css_class='form-group col-md-6 mb-0'),
                # Column('status', css_class='form-group col-md-6 mb-0'),
            ),
            Row(
                Column('reason', css_class='form-group col-md-12 mb-0'),
            ),
            HTML(""" <div class="text-left mt-4"> <button class="btn btn-sm btn-labeled btn-info" type="submit" title="Update"><span class="btn-label"><i class='fa fa-save'></i></span> Save</button>"""),
            HTML("""  <button class="btn btn-sm btn-labeled btn-secondary" onclick=self.history.back()><span class="btn-label"><i class="fa fa-window-close"></i></span> Cancel</button></div>""")
        )

class SearchForm(forms.Form):
    field = forms.ChoiceField(choices=[
        ('nu_id', 'ID'),
        ('nome_completo', 'Nome Completo'),
        ('sexo', 'Sexo'),
        ('naturalidade', 'Naturalidade'),
        ('data_do_nasc', 'Data de Nascimento'),
        ('data_entrada', 'Data de Entrada'),
        ('validade', 'Validade'),
        ('posição', 'Posição'),
        ('endereço', 'Endereço'),
        ('município', 'Município'),
        ('estatuto', 'Estatuto'),
        ('estatus_onoff', 'Estatus ON/OFF'),
        ('nu_contacto', 'Contacto'),
        ('email', 'Email')
    ])
    condition = forms.ChoiceField(choices=[
        ('contains', 'Contains'),
        ('equals', 'Equals')
    ])
    value = forms.CharField(max_length=200)