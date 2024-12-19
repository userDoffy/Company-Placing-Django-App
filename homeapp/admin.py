from django.contrib import admin

from homeapp.models import Student,Company

# Register your models here.
admin.site.register(Company)
admin.site.register(Student)