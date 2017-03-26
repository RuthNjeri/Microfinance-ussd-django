from django.db import models

# Create your models here.

class Microfinance(models.Model):
	name = models.CharField(max_length=30)
	phonenumber = models.CharField(max_length=20)
	city = models.CharField(max_length=30)
	validation = models.CharField(max_length=30)
	reg_date=models.IntegerField()

class session_levels(models.Model):
	  session_id = models.CharField(max_length=50)
	  phonenumber= models.CharField(max_length=25)
	  level = models.IntegerField()	