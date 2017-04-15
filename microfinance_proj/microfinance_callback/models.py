from django.db import models

# Create your models here.

class Microfinance(models.Model):
	name = models.CharField(max_length=30,null=True)
	phonenumber = models.CharField(max_length=20,null=True)
	city = models.CharField(max_length=30,null=True)
	reg_date=models.DateField(auto_now_add=True)
	level = models.IntegerField(null=True)
	

class session_levels(models.Model):
	  session_id = models.CharField(max_length=25,primary_key=True)
	  phonenumber= models.CharField(max_length=25,null=True)
	  level = models.IntegerField(null=True)	

class account(models.Model):
		phonenumber= models.CharField(max_length=25,null=True)
		balance= models.IntegerField(null=True)
		loan= models.IntegerField(null=True)
		reg_date= models.DateField(auto_now_add=True)

class checkout(models.Model):
		status=models.CharField(max_length=30,null=True)
		phonenumber=models.CharField(max_length=30,null=True)
		amount = models.IntegerField(null=True)
		reg_date=models.DateField(auto_now_add=True)
		