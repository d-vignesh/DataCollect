from django.contrib import admin
from .models import Person, OperationStatus

# Register your models here.
admin.site.register(Person)
admin.site.register(OperationStatus)
