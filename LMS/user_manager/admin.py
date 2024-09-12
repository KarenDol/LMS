from django.contrib import admin
from .models import Student, Curator, Admin, Parent, Contract, List_Of_Students
# Register your models here.

admin.site.register(Student)
admin.site.register(Curator)
admin.site.register(Admin)
admin.site.register(Parent)
admin.site.register(Contract)
admin.site.register(List_Of_Students)