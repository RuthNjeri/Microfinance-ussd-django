from django.db import models

# Create your models here.

class Microfinance(models.Model):
	name = models.CharField(max_length=30)
	phonenumber = models.CharField(max_length=20)
	city = models.CharField(max_length=30)
	validation = models.CharField(max_length=30)
	reg_date=models.DateField(auto_now_add=True)

class session_levels(models.Model):
	  session_id = models.CharField(max_length=60,primary_key=True)
	  phonenumber= models.CharField(max_length=25)
	  level = models.IntegerField()	

class account(models.Model):
		phonenumber= models.CharField(max_length=25)
		balance= models.DecimalField(max_digits=5,decimal_places=2)
		loan= models.DecimalField(max_digits=5,decimal_places=2)
		reg_date= models.DateField(auto_now_add=True)
		