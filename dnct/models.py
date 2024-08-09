from django.db import models
from custom.models import *
from datetime import timedelta, date
from django.core.exceptions import ValidationError
# Create your models here.

class Department(models.Model):
    name = models.CharField(max_length=100)
    sigla = models.CharField(max_length=100,default='default')
    manager = models.ForeignKey('funcionariu', on_delete=models.SET_NULL, null=True, related_name='department')
    location = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Funcionariu(models.Model):
	nu_id = models.CharField(max_length=20,unique=True,null=True)
	nome_completo = models.CharField(max_length=200,null=True)
	sexo = models.CharField(choices=[('Mane','Mane'),('Feto','Feto')],max_length=10,null=True,blank=True)
	naturalidade = models.CharField(max_length=200,null=True)
	data_do_nasc = models.DateField(null=True)
	data_entrada = models.DateField(null=True)
	validade = models.DateField(null=True)
	direction = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
	posição = models.CharField(max_length=200,null=True)
	endereço = models.CharField(max_length=200,null=True)
	município = models.ForeignKey(Municipality, on_delete=models.CASCADE,null=True)
	estatuto = models.ForeignKey(Status, on_delete=models.CASCADE,null=True)
	nivel_estudo = models.ForeignKey(Nivel_Estudo, on_delete=models.CASCADE,null=True)
	especialidade = models.CharField(max_length=200,null=True)
	grau = models.CharField(max_length=200,null=True)
	estatus_onoff = models.ForeignKey(Estatus, on_delete=models.CASCADE,null=True)
	nu_contacto = models.CharField(max_length=200,null=True)
	email = models.EmailField(max_length=200,null=True)
	fotografia = models.ImageField(upload_to='images/',null=True, blank=True)
	documentos = models.FileField(upload_to='CV/', null=True, blank=True)

	def __str__(self):
		return self.nome_completo

	def get_age(self):
		import datetime
		age = datetime.date.today().year-self.data_do_nasc.year
		return age
    
def is_birthday_today(self):
        today = date.today()
        return (self.data_do_nasc.month == today.month and self.data_do_nasc.day == today.day)

class Salary(models.Model):
    employee = models.ForeignKey(Funcionariu, on_delete=models.CASCADE)
    salary_amount = models.DecimalField(max_digits=10, decimal_places=2)
    effective_date = models.DateField()

    def __str__(self):
        return f"{self.employee.nome_completo} - {self.salary_amount} ({self.effective_date})"

class Attendance(models.Model):
    employee = models.ForeignKey(Funcionariu, on_delete=models.CASCADE)
    date = models.DateField()
    time_in = models.TimeField()
    time_out = models.TimeField()
    total_hours = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.employee.nome_completo} - {self.date}"


class Leave(models.Model):
    LEAVE_CHOICES = [
        ('Licença', 'Licença'),
        ('Licença Annual', 'Licença Annual'),
        ('Licença do Casamento', 'Licença do Casamento'),
        ('Licença do Estudo', 'Licença do Estudo'),
        ('Licença de Luto', 'Licença de Luto'),
        ('Licença de Maternidade', 'Licença de Maternidade'),
        ('Licença de Paternidade', 'Licença de Paternidade'),
        ('Licença Sem Vencimento', 'Licença Sem Vencimento'),
        ('Doente', 'Doente'),
        ('Licença de Consulta Médica', 'Licença de Consulta Médica'),
        ('Missão de Serviço', 'Missão de Serviço'),
        ('Tolerância de Ponto', 'Tolerância de Ponto'),
    ]

    employee = models.ForeignKey(Funcionariu, on_delete=models.CASCADE)
    leave_type = models.CharField(max_length=200, choices=LEAVE_CHOICES)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=200, editable=False)  # Remove default value and make it non-editable
    reason = models.TextField()
    archived = models.BooleanField(default=False)

    def clean(self):
        total_days = self.calculate_weekdays(self.start_date, self.end_date)
        if self.leave_type == 'Licença' and total_days > 3:
            raise ValidationError('A licença está limitada a 3 dias.')
        elif self.leave_type == 'Licença do Casamento' and total_days > 5:
            raise ValidationError('A Licença de Casamento está limitada a 5 dias.')
        elif self.leave_type == 'Licença Annual' and total_days > 20:
            self.validate_annual_leave()
        elif self.leave_type == 'Licença do Estudo' and (self.end_date - self.start_date).days / 365 > 4:
            raise ValidationError('A Licença de Estudo está limitada a 4 anos.')
        elif self.leave_type == 'Licença de Luto' and total_days > 5:
            raise ValidationError('A Licença de Luto está limitada a 5 dias.')
        elif self.leave_type == 'Licença de Maternidade' and total_days > 67:  # 66 working days for 3 months
            raise ValidationError('A Licença de Maternidade está limitada a 3 meses.')
        elif self.leave_type == 'Licença de Paternidade' and total_days > 5:
            raise ValidationError('A Licença de Paternidade está limitada a 5 dias')
        elif self.leave_type == 'Licença Sem Vencimento' and (self.end_date - self.start_date).days / 365 > 2:
            raise ValidationError('A Licença Sem Vencimento está limitada a 2 anos.')
        elif self.leave_type == 'Doente' and total_days > 3:
            raise ValidationError('Doente está limitado a 3 dias. Se for superior a 3 dias, é necessário comprovar o exame médico.')

    def validate_annual_leave(self):
        start_year = self.start_date.year
        end_year = self.end_date.year
        if start_year != end_year:
            raise ValidationError('A Licença Anual não deve exceder os anos civis.')

        year_leaves = Leave.objects.filter(employee=self.employee, leave_type='Licença Annual', start_date__year=start_year)
        total_days = sum(self.calculate_weekdays(leave.start_date, leave.end_date) for leave in year_leaves)
        if total_days + self.calculate_weekdays(self.start_date, self.end_date) > 20:
            raise ValidationError('A Licença Anual está limitada a 20 dias por ano.')

        start_month = self.start_date.month
        end_month = self.end_date.month
        if start_month == end_month:
            month_leaves = year_leaves.filter(start_date__month=start_month)
            month_days = sum(self.calculate_weekdays(leave.start_date, leave.end_date) for leave in month_leaves)
            if month_days + self.calculate_weekdays(self.start_date, self.end_date) > 10:
                raise ValidationError('A Licença Anual está limitada a 10 dias num único mês.')

    def calculate_weekdays(self, start_date, end_date):
        total_days = (end_date - start_date).days + 1
        weekdays_count = sum(1 for i in range(total_days)
                             if (start_date + timedelta(days=i)).weekday() < 5)
        return weekdays_count

    def calculate_leave_days(self):
        current_date = date.today()
        if current_date > self.end_date:
            self.status = 'O tempo de licença acabou'
            return 0

        total_days = self.calculate_weekdays(self.start_date, self.end_date)
        if total_days > 10:
            total_days = 10

        return total_days

    def update_status(self):
        current_date = date.today()
        if current_date > self.end_date:
            self.status = 'O tempo de licença acabou'
        else:
            self.status = 'Licença'

    def save(self, *args, **kwargs):
        self.update_status()  # Update status before saving
        self.full_clean()  # Ensure clean() is called to validate the model
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.employee.nome_completo} - {self.leave_type} ({self.start_date} to {self.end_date})"


class Training(models.Model):
    employee = models.ForeignKey(Funcionariu, on_delete=models.CASCADE)
    training_type = models.CharField(max_length=100)
    trainer = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    location = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.employee.nome_completo} - {self.training_type} ({self.start_date} to {self.end_date})"


class Performance(models.Model):
    employee = models.ForeignKey(Funcionariu, on_delete=models.CASCADE)
    review_date = models.DateField()
    reviewer = models.CharField(max_length=100)
    ratings = models.DecimalField(max_digits=3, decimal_places=1)
    comments = models.TextField()

    def __str__(self):
        return f"{self.employee.nome_completo} - {self.review_date}"

		



