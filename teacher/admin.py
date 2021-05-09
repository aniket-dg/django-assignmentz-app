from django.contrib import admin
from .models import Teacher, Assignment_Q, Status
# Register your models here.
admin.site.register(Teacher)
admin.site.register(Assignment_Q)
admin.site.register(Status)