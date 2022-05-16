from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.mail import send_mail, BadHeaderError
from django.contrib import messages  # Message Framework
from django.contrib.auth.forms import PasswordResetForm
from assignment.settings import BASE_DIR, EMAIL_HOST_USER, EMAIL_TEMPLATE
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.db.models import Q
from os import path
from teacher.models import Teacher
from student.models import Student


# Create your views here.
def login_student(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            userName = request.POST['userName']
            password = request.POST['passWord']
            user = authenticate(request, email=userName, password=password)
            if user is not None:
                if is_teacher(user.id):
                    messages.error(request, 'Please select appropriate User Role')
                    return redirect(home)
                else:
                    if is_student(user.id):
                        login(request, user)
                        return redirect('/student')
                    else:
                        messages.warning(request, 'Student Not Found !')
                        return redirect('/login')
            else:
                messages.warning(request, "Invalid Login Credentials")
                return redirect('/login/login_student')
        else:
            return render(request, 'login/student_login.html')
    else:
        return redirect('/student')


def is_student(id):
    try:
        student = Student.objects.get(student_id=id)
        return True
    except Exception as e:
        return False


def is_teacher(id):  # Check User is Teacher or Not
    try:
        teacher = Teacher.objects.get(teacher_id=id)
        return True
    except Exception as e:
        return False


def login_teacher(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            email = request.POST['email']
            password = request.POST['passWord']
            user = authenticate(email=email, password=password)
            if user is not None:
                if is_teacher(user.id):
                    login(request, user)
                    return redirect('/teacher')
                else:
                    messages.warning(request, "You are not authorized to access Teacher Account")
                    return redirect(home)
            else:
                messages.warning(request, "Invalid Login Credentials")
                return redirect('/login/login_teacher')
        else:
            return render(request, 'login/teacher_login.html')
    else:
        return redirect('/teacher')


def is_super(id):
    try:
        super_user = User.objects.get(id=id)
        if super_user.is_superuser:
            return True
        else:
            return False
    except Exception as e:
        return False


def home(request):
    if request.user.is_authenticated:
        if is_teacher(request.user.id):
            return redirect('/teacher')
        else:
            if is_student(request.user):
                return redirect('/student')
            else:
                return redirect('/admin')
    else:
        return render(request, 'login/home.html')


@login_required
def change_password(request):
    if request.method == "POST":
        user = User.objects.get(id=request.user.id)
        user.set_password(request.POST['newPassword'])
        user.save()
        logout(request)
        messages.success(request, "Password Change Successfully........")
        return redirect('home')
    else:
        return HttpResponse("System Error")


@login_required
def change_password_view(request):
    return render(request, 'login/change_password.html')


def logout_user(request):
    logout(request)
    return redirect('home')
