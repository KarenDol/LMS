from django.db import models
from django.contrib.auth.models import User
from .const import Grades_models

#Create your models here.
class Parent(models.Model):
    #crucial
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    Last_Name = models.CharField(max_length=40)
    First_Name = models.CharField(max_length=30)
    Patronim = models.CharField(max_length=40, null=True)
    Phone = models.CharField(max_length=20)
    ID_number = models.CharField(max_length=9) #Номер Удостоверения
    ID_date = models.DateField()
    ID_org = models.CharField(max_length=30) #Кем Выдан

    #not crucial
    Address = models.CharField(max_length=100, null=True) #Адрес проживания
    Working_Place = models.CharField(max_length=30, null=True)
    Position = models.CharField(max_length=30, null=True)

class Contract(models.Model):
    numb = models.CharField(max_length=20, primary_key=True)
    sign_date = models.DateField() #Дата подписания
    first_date = models.DateField() #Вступает в силу
    last_date = models.DateField() #Последний день договора
    total = models.IntegerField() #Общая стоимость
    discount = models.IntegerField() #С учетом льгот и скидок
    monthly = models.IntegerField() #Ежемесячная оплата
    join_fee = models.IntegerField() #Вступительные
    location = models.CharField(max_length=150) #Location of file
    status = models.CharField(max_length=50, choices=[
        ('Под', 'Подписан'),
        ('НеПод', 'Не подписан'),
    ], default='НеПод')

class Student(models.Model):
    #crucial
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    Last_Name = models.CharField(max_length=40)
    First_Name = models.CharField(max_length=30)
    Patronim = models.CharField(max_length=40, null=True)
    birthdate = models.DateField()
    IIN = models.CharField(max_length=12)
    grade = models.CharField(max_length=3, choices=Grades_models, default='-')
    parent_1 = models.ForeignKey(Parent, on_delete=models.CASCADE, null=True, related_name='mom')
    # parent_2 = models.ForeignKey(Parent, on_delete=models.CASCADE, null=True, related_name='dad')
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE, null=True)

    #not crucial
    nationality = models.CharField(max_length=20, null=True)
    prev_school = models.CharField(max_length=50, null=True)
    phone = models.CharField(max_length=20, null=True)
    comment = models.CharField(max_length=200, null=True)

class Curator(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    curator_class1 = models.CharField(max_length=2, blank=True, null=True)
    curator_class2 = models.CharField(max_length=2, blank=True, null=True)
    curator_class3 = models.CharField(max_length=2, blank=True, null=True)

class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    picture = models.CharField(max_length=150, null=True)

class List_Of_Students(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE)
    Last_Name = models.CharField(max_length=40) #Фамилия ученика
    First_Name = models.CharField(max_length=30) #Имя ученика
    Class = models.CharField(max_length=30) #Класс ученика
    Phone = models.CharField(max_length=20) #Номер Родителя
    Payment = models.IntegerField() #Ежемесячная Оплата
    Sep = models.IntegerField(default=0) #Оплачено за сентябрь
    Oct = models.IntegerField(default=0)
    Nov = models.IntegerField(default=0)
    Dec = models.IntegerField(default=0)
    Jan = models.IntegerField(default=0)
    Mar = models.IntegerField(default=0)
    Apr = models.IntegerField(default=0)
    May = models.IntegerField(default=0)