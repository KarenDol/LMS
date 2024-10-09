from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.forms.models import model_to_dict
from django.http import FileResponse, Http404
from .models import Student, Parent, Contract, List_Of_Students, LMS_User
from django.db import IntegrityError
import datetime
import requests
from .dogovor import fill_doc
from .const import Grades, Grades_dict, Grades_home, User_type_dict
import json
import os
from django.http import JsonResponse

# Create your views here.
def home(request):
    if (not user_auth(request)):
        return redirect('logout')
    students = list(Student.objects.all().values('Last_Name', 'First_Name', 'Patronim', 'IIN', 'phone', 'grade', 'status'))
    students_json = json.dumps(students)
    Grades_dict_json = json.dumps(Grades_dict)

    #Populating context
    context = {
        'Grades': Grades_home, 
        'Grades_dict': Grades_dict_json, 
        'students': students_json,
    }

    return render(request, 'home.html', context)

#Fetch all user info
def user_auth(request):
    if request.user.is_authenticated:
        try:
            current_user = LMS_User.objects.get(user=request.user)
            return True
        except LMS_User.DoesNotExist:
            messages.error(request, "User is not LMS User")
            return False
    else:
        messages.error(request, "Login to access that page")
        return False

#Check if student exists or not    
def student_exist(IIN):
    try:
        student = Student.objects.get(IIN=IIN)
        return True
    except Student.DoesNotExist:
        return False

def parent_exist(IIN):
    if student_exist(IIN):
        student = Student.objects.get(IIN=IIN)
        parent = student.parent_1
        if parent:
            return True
        else:
            return False
    else:
        return False

def contract_exist(IIN):
    if parent_exist(IIN):
        student = Student.objects.get(IIN=IIN)
        contract = student.contract
        if contract:
            return True
        else:
            return False
    else:
        return False

#Fetch the name and the picture of the user for the index.html
def get_user_info(request):
    current_user = LMS_User.objects.get(user=request.user)
    user_info = {
        'name': current_user.name,  
        'picture': current_user.picture,
    }
    return JsonResponse(user_info)

#GET the static file
def serve_static(request, filename):
    file_path = os.path.join(settings.STATIC_ROOT, filename)

    if os.path.exists(file_path):
        return FileResponse(open(file_path, 'rb'))
    else:
        raise Http404("Avatar not found.")

def login_user(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == "POST":
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, "Login failed. Please check your username and password.")
                return redirect('login_user')
        else:
            return render(request, 'login.html')

def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out!")
    return redirect('login_user')

def register_student(request):
    if (not user_auth(request)):
        return redirect('logout')
    
    current_user = LMS_User.objects.get(user=request.user)
    if current_user.user_type == 'ВнСв':
        if request.method == "POST":
            lastname = request.POST['lastname']
            firstname = request.POST['firstname']
            patronim = request.POST['patronim']
            birthdate = request.POST['birthdate']
            IIN = request.POST['IIN']
            grade = Grades_dict[request.POST['grade']]
            nationality = request.POST['nationality']
            prev_school = request.POST['prev_school']                
            phone = request.POST['phone']
            comment = request.POST['comment']

            #Check if student already exists
            if student_exist(IIN):
                return redirect('error', error_code='Ученик c таким ИИН уже добавлен в систему')
            new_user = User(username=IIN, first_name=firstname)
            new_user.set_password("AIS@100")
            new_user.save()
            new_student = Student(user=new_user, Last_Name=lastname, First_Name=firstname, Patronim=patronim, phone=phone,
                            birthdate=birthdate, IIN=IIN, prev_school=prev_school, grade=grade, nationality=nationality,
                            comment=comment)
            new_student.save()
            messages.success(request, "New Student Has Been Added")
            return redirect('register_parent', IIN=new_student.IIN)
        else:
            context = {
                'Grades': Grades
            }
            return render(request, 'register_student.html', context)
    else:
        messages.success(request, "Only ВнСв can add new students")
        return redirect('home')


def register_parent(request, IIN):
    if (not user_auth(request)):
        return redirect('logout')
    if student_exist(IIN):
        new_student = Student.objects.get(IIN=IIN)
    else:
        return redirect('error', error_code='Ученика с таким ИИН нет в системе')
    if parent_exist(IIN): #If parent already exists
        return redirect('error', error_code='Родитель данного ученика уже добавлен в систему')
    current_user = LMS_User.objects.get(user=request.user)
    if current_user.user_type == 'ВнСв':
        if request.method == 'POST':
            First_Name = request.POST['firstname']
            Last_Name = request.POST['lastname']                
            Patronim = request.POST['patronim']
            Phone = request.POST['phone']
            ID_number = request.POST['ID_number']
            new_user = User(username="parent_" + ID_number, first_name=First_Name)
            new_user.set_password("AIS@100")
            new_user.save()
            ID_org = request.POST['ID_org']
            ID_date = request.POST['ID_date']
            Place = request.POST['workplace']
            Position = request.POST['position']
            address = request.POST['address']
            new_parent = Parent(user=new_user, First_Name=First_Name, Last_Name=Last_Name, Patronim=Patronim,
                        Phone=Phone, ID_number=ID_number, ID_org=ID_org, ID_date=ID_date,
                        Working_Place=Place, Position=Position, Address=address)
            new_parent.save()
            new_student.parent_1 = new_parent
            new_student.save()
            return redirect('register_contract', IIN=IIN)            
        else:
            context = {
                'IIN': IIN,
            }
            return render(request, 'register_parent.html', context)
    else:
        messages.success(request, "Only ВнСв can add new students")
        return redirect('home')

def register_contract(request, IIN):
    if (not user_auth(request)):
        return redirect('logout')
    if parent_exist(IIN):
        new_student = Student.objects.get(IIN=IIN)
    else:
        return redirect('error', "Сначала убедитесь, что студент и родитель добавлены в систему")
    current_user = LMS_User.objects.get(user=request.user)
    if contract_exist(IIN): #If contract already exists
        return redirect('error', error_code='Договор для данного ученика уже составлен')
    if current_user.user_type == 'ВнСв':
        if request.method == 'POST':
            date = str(datetime.datetime.now())
            numb = date[2:4] + date[5:7] + date[8:10] + date[11:13] + date[14:16] + date[17:19]
            sign_date = request.POST['sign_date']
            first_date = request.POST['first_date']
            last_date = request.POST['last_date']
            total = request.POST['total']
            discount = request.POST['discount']
            monthly = request.POST['monthly']
            join_fee = request.POST['join_fee']
            new_student = Student.objects.get(IIN=IIN)
            new_contract = Contract(numb=numb, sign_date=sign_date, first_date=first_date, last_date=last_date,
                                    total=total, discount=discount, monthly=monthly, join_fee=join_fee,
                                    template_location='dogovor' + str(numb) + '.pdf')
            new_contract.save()
            new_student.contract = new_contract
            new_student.status = 'Акт'
            new_student.save()
            fill_doc(IIN)
            return redirect('sign_doc', IIN=IIN)
        else:
            context = {
                'IIN': IIN, 
                'today': str(datetime.date.today()),
            }
            return render(request, 'register_contract.html', context)
    else:
        messages.success(request, "Only ВнСв can add new students")
        return redirect('home')



def send_sms(phones, message):
    # API endpoint URL
    api_url = "https://smsc.kz/sys/send.php"

    # Construct the parameters
    params = {
        'login': 'aqbobek',
        'psw': 'kAREN_2001',
        'phones': phones,
        'mes': message,
    }

    try:
         # Make the HTTP request
        response = requests.get(api_url, params=params)
         # Check the response status code
        if response.status_code == 200:
            print(response.status_code)
            # SMS sent successfully
            print("SMS was sent succesfully")
            return True
        else:
            # Handle any errors
            print("SMS was not sent")
            return False

    except requests.RequestException as e:
        # Handle request exceptions
        print(f"Request error: {e}")

def delete_student(request, pk):
    if request.user.is_authenticated:
        delete_it = Student.objects.get(id=pk)
        delete_it.delete()
        delete_it = User.objects.get(id=pk)
        delete_it.delete()
        messages.success(request, "Student Deleted Successfully")
    else:
        messages.success(request, "You Must Be Logged In To Delete The Record")
    return redirect('home')

def student_card(request, IIN):
    if (not user_auth(request)):
        return redirect('logout')
    if student_exist(IIN):
        student = Student.objects.get(IIN=IIN)
    else:
        return redirect('error', error_code='Похоже. что ученика с таким ИИН нет в системе')
    context = {
        'student': student,
    }
    return render(request, 'student_card.html', context)

def parent_card(request, IIN):
    if (not user_auth(request)):
        return redirect('logout')
    if parent_exist(IIN):
        student = Student.objects.get(IIN=IIN)
    else:
        return redirect('error', error_code='Похоже. что родитель данного ученика еще не добавлен в систему')
    parent = student.parent_1
    context = {
        'parent': parent,
    }
    return render(request, 'parent_card.html', context)

def contract_card(request, IIN):
    if (not user_auth(request)):
        return redirect('logout')
    if contract_exist(IIN):
        student = Student.objects.get(IIN=IIN)
    else:
        return redirect('error', error_code='Похоже. что данного договора нет')
    contract = student.contract
    dogovor_temp = contract.template_location
    dogovor_temp = os.path.join('docs', dogovor_temp)
    dogovor_sign = contract.signed_location
    if dogovor_sign:
        dogovor_sign = os.path.join('docs', dogovor_sign)
    context = {
        'contract': contract,
        'dogovor_temp': dogovor_temp,
        'dogovor_sign': dogovor_sign,
        'IIN': IIN,
    }
    return render(request, 'contract_card.html', context)

def sign_doc(request, IIN):
    if (not user_auth(request)):
        return redirect('logout')
    student = student_exist(IIN)
    contract = student.contract
    dogovor = os.path.join('docs', contract.template_location)
    folder_path = os.path.join(settings.STATIC_ROOT, 'docs')
    if request.method == "POST":
        for name, file in request.FILES.items():
            file = request.FILES.get(name)
            fs = FileSystemStorage(location=folder_path)
            fs.save(file.name, file)
            contract.signed_location = (file.name)
        contract.save()
        return redirect('home')
    else:
        context = {
            'contract': contract,
            'dogovor': dogovor,
            'IIN': IIN,
        }
        return render(request, 'sign_doc.html', context)

def finance(request):
    if request.user.is_authenticated:
        try:
            admin = Admin.objects.get(user=request.user)
            my_list = Student.objects.order_by('Class', 'Last_Name', 'First_Name')
            my_list = list(my_list)
            n=int(datetime.datetime.now().strftime("%m"))
            return render(request, 'finance.html', {'role': 'curator', 'n': n, 'my_list': my_list})
        except Admin.DoesNotExist:
            student = Student.objects.get(user=request.user)
            return render(request, 'home.html', {'role': 'student', 'cur_user': student})
    else:
        messages.success(request, "Login in to access that page")
        return redirect('login_user')

def cash(request, entr_id):
    if request.user.is_authenticated:
        try:
            admin = Admin.objects.get(user=request.user)
            entry = List_Of_Students.objects.get(pk=entr_id)
            if request.method == 'POST':
                month = request.POST['month']
                payment = request.POST['payment']
                payment = int(payment)
                if month=='Сентябрь':
                    entry.Sep += payment
                elif month=='Октябрь':
                    entry.Oct += payment
                elif month == 'Ноябрь':
                    entry.Nov += payment
                elif month == 'Декабрь':
                    entry.Dec += payment
                elif month == 'Январь':
                    entry.Jan += payment
                elif month == 'Февраль':
                    entry.Feb += payment
                    entry.save()
                elif month == 'Март':
                    entry.Mar += payment
                    entry.save()
                elif month == 'Апрель':
                    entry.Apr += payment
                elif month == 'Май':
                    entry.May += payment
                entry.save()
                print(month, payment)
                return redirect('home')
            else:
                return render(request, 'cash.html', {'student': entry, 'entr_id':entr_id})
        except Admin.DoesNotExist:
            student = Student.objects.get(user=request.user)
            return render(request, 'home.html', {'role': 'student',
                                                 'cur_user': student})
    else:
        messages.success(request, "Login in to access that page")
        return redirect('login_user')

def user_settings(request):
    if request.user.is_authenticated:
        current_user = LMS_User.objects.get(user=request.user)
        if request.method == "POST":
            try:
                new_username = request.POST['username']
                if new_username and new_username != current_user.user.username:
                    current_user.user.username = new_username
                    current_user.user.save()
                
                oldPassword = request.POST['oldPassword']
                newPassword = request.POST['newPassword']
                if oldPassword:
                    user = authenticate(username = request.user.username, password = oldPassword)
                    print(request.user.username, oldPassword)
                    if user is not None:
                        user.set_password(newPassword)
                        user.save()
                    else:
                        print("WrongPassword")
                
                new_email = request.POST['email']
                if new_email and new_email != current_user.email:
                    current_user.email = new_email
                
                new_phone = request.POST['phone']
                if new_phone and new_phone != current_user.phone:
                    current_user.phone = new_phone

                if 'avatar' in request.FILES:
                    new_avatar = request.FILES['avatar']
                    folder_path = os.path.join(settings.STATIC_ROOT, 'avatars')

                    fs = FileSystemStorage(folder_path)
                    fs.save(new_avatar.name, new_avatar)


                    current_user.picture = os.path.join('avatars', new_avatar.name)
                
                current_user.save()
                
                
                
                # Send success response
                return JsonResponse({'status': 'success', 'message': 'Settings updated successfully'}, status=200)
            except Exception as e:
                # Handle exceptions and return an error response
                print(f"Error occurred: {e}")
                return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
        else:
            user_dict = model_to_dict(current_user, fields=['name', 'phone', 'email', 'picture'])
            user_dict['position'] = User_type_dict[current_user.user_type]
            user_dict['username'] = current_user.user.username
            return render(request, 'user_settings.html', {'user_dict': user_dict})
    else:
        return redirect('login')
    
def error(request, error_code):
    return render(request, '404.html', {'error_code': error_code})