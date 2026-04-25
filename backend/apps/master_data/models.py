from django.db import models

class Country(models.Model):
    name = models.CharField(max_length=100)
    iso_code = models.CharField(max_length=10)
    def __str__(self): return self.name

class Province(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

class District(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20)
    province = models.ForeignKey(Province, on_delete=models.CASCADE)

class Ward(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20)
    district = models.ForeignKey(District, on_delete=models.CASCADE)

class Career(models.Model):
    name = models.CharField(max_length=100)

class EthnicGroup(models.Model):
    name = models.CharField(max_length=50)

class Specialty(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    img = models.ImageField(upload_to='specialties/', null=True, blank=True)

class Disease(models.Model):
    code = models.CharField(max_length=20)
    name = models.CharField(max_length=255)

class LabService(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=12, decimal_places=2)