from django.db import models

# Create your models here.
class Tinan(models.Model):
	tinan = models.CharField(max_length=4,null=True)
	status = models.BooleanField(default=True)

	def __str__(self):
		return self.tinan

class Status(models.Model):
	name = models.CharField(max_length=32, null=True)

	def __str__(self):
		template = '{0.name}'
		return template.format(self)
		
# class Tinan(models.Model):
# 	tinan = models.CharField(max_length=4,null=True)

# 	def __str__(self):
# 		return self.tinan
class Municipality(models.Model):
	code = models.CharField(max_length=5, null=True, blank = True)
	name = models.CharField(max_length=100)
	hckey = models.CharField(max_length=32, null=True ,  blank = True)
	def __str__(self):
		template = '{0.name}'
		return template.format(self)

class AdministrativePost(models.Model):
	municipality = models.ForeignKey(Municipality, on_delete=models.CASCADE, null=True)
	name = models.CharField(max_length=100)
	def __str__(self):
		template = '{0.name}'
		return template.format(self)

class Village(models.Model):
	administrativepost = models.ForeignKey(AdministrativePost, on_delete=models.CASCADE, null=True)
	name = models.CharField(max_length=100)
	def __str__(self):
		template = '{0.name}'
		return template.format(self)

class Aldeia(models.Model):
	village = models.ForeignKey(Village, on_delete=models.CASCADE, null=True)
	name = models.CharField(max_length=100)
	def __str__(self):
		template = '{0.name}'
		return template.format(self)

class AcademicLevel(models.Model):
	name = models.CharField(max_length=50, verbose_name="Naran")
	def __str__(self):
		template = '{0.name}'
		return template.format(self)

class Religion(models.Model):
    name = models.CharField(max_length = 50,verbose_name='Relijiaun')
    def __str__(self):
        template = '{0.name}'
        return template.format(self)

    class Meta:
        verbose_name_plural='Dadus Custom Ba Relijiaun'


class Estatus(models.Model):
    STATUS_CHOICES = [
        ('Ativo', 'Ativo'),
        ('Licença', 'Licença'),
        ('Desiste', 'Desiste'),
        ('Reforma', 'Reforma'),
    ]

    estatus = models.CharField(max_length=20,choices=STATUS_CHOICES,default='Ativo',)

    def __str__(self):
        return self.get_estatus_display()
