from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from login.views import is_teacher, logout_user, is_student, is_super
from .models import Teacher, Assignment_Q, Status
from database.models import Course
from student.models import Assignment_Ans, Student
import json
from django.contrib import messages
from django.contrib.auth import logout
# Create your views here.
@login_required(login_url='/login/login_student')
def dashboard(request):
    if is_teacher(request.user.id):
        course_list = getAssignedCourse(request, request.user.id)
        teacher = Teacher.objects.get(teacher_id = request.user.id)
        assignment_list = Assignment_Q.objects.filter(teacher_id = teacher)
        status = getStatus(request, teacher)
        total = getAssignment(request, teacher)
        assignment_list_with_status = zip(assignment_list, status)
        return render(request, 'teacher/dashboard.html', { 'course_list': course_list , 'assignment_list_with_status': assignment_list_with_status, 'total':total })
    else:
        logout(request)
        return redirect('home')

def getAssignment(request, teacher):
    if is_teacher(request.user.id):
        a = Assignment_Q.objects.filter(teacher_id = teacher).count()
        return a
    else:
        logout(request)
        return redirect('home')


def getStatus(request, teacher):
    if is_teacher(request.user.id):
        assignment = Assignment_Q.objects.filter(teacher_id = teacher)
        status = []
        for assignment in assignment:
            status.append(Status.objects.filter(assignment_id = assignment))
        result = []
        for s in status:
            for y in s:
                result.append(y)
        return result
    else:
        logout(request)
        return redirect('home')



def getAssignedCourse(request, id):#Get the Course Name Which Faculty teach
    if is_teacher(request.user.id):
        try:
            user = Teacher.objects.get(teacher_id = id)
            courses = user.asssigned_course.all()
            return courses
        except:
            return HttpResponse("Error")
    else:
        logout(request)
        return redirect('home')
    

def getUser(request):#Get Super User
    if is_teacher(request.user.id):
        return User.objects.get(id = request.user.id)
    else:
        logout(request)
        return redirect('home')

def getProfile(request):# Profile Details and Updation
    if is_teacher(request.user.id):
        user = getUser(request)
        course = getAssignedCourse(request,request.user.id)
        if request.method == "POST":
            if request.POST['teacher_name'] != '':
                user.first_name = request.POST['teacher_name']
                user.save()
            if request.POST['newPassword'] != '':
                try:
                    user.set_password(request.POST['newPassword'])
                    user.save()
                    return redirect(logout_user)
                except Exception as e:
                    return HttpResponse(e)
            messages.success(request, "Profile Updated Successfully")
            return redirect('/teacher/profile')
        else:
            return render(request, 'teacher/profile.html',{ 'user':user, 'course':course })
    else:
        logout(request)
        return redirect('home')
    
    
def course(request, id):
    if is_teacher(request.user.id):
        course = Course.objects.get(id=int(id))
        teacher = Teacher.objects.get(teacher_id = request.user.id)
        assignments = Assignment_Q.objects.filter(teacher_id = teacher)
        status = getStatus(request, teacher)
        assignments_with_status = zip(assignments, status)
        return render(request, 'teacher/subject.html', { 'course': course, 'assignments_with_status': assignments_with_status })
    else:
        logout(request)
        return redirect('home')

def create_assignment(request, id):
    if is_teacher(request.user.id):
        course = Course.objects.get(id=int(id))
        return render(request, 'teacher/generate.html', {'course':course})
    else:
        logout(request)
        return redirect('home')

def assignment_submit(request, id):
    if is_teacher(request.user.id):
        data = request.POST['questions']
        assignment_no = request.POST['no']
        assignment_name = request.POST['name']
        last_date = request.POST['last_date']
        question = data.strip().splitlines()
        question_json = json.dumps(question)
        teacher = Teacher.objects.get(teacher_id = int(request.user.id))
        course = Course.objects.get(id = id)
        assignment = Assignment_Q.objects.create(teacher_id = teacher, assignment_name = assignment_name,last_date = last_date, question_list = question_json, course_id = course, assignment_no = assignment_no)
        assignment.save()
        assignment = Assignment_Q.objects.filter(teacher_id = teacher, assignment_no = assignment_no)
        status = Status.objects.create(teacher_id = teacher, course_id= course, assignment_id = assignment[0])
        remaining_student = Student.objects.all().count()
        status.remaining_student = remaining_student
        status.save()
        url = '/teacher/course/{0}'.format(course.id)
        messages.success(request, "Assignment Created Successfully !")
        return redirect(url)
    else:
        logout(request)
        return redirect('home')

def assignment_view(request, course_id, assignment_id):
    if is_teacher(request.user.id):
        assignments = Assignment_Q.objects.filter(id = assignment_id)
        course = Course.objects.get(id = course_id)
        questions = json.loads(assignments[0].question_list)
        return render(request, 'teacher/assignment_view.html', { 'course':course, 'assignments':assignments, 'questions':questions })
    else:
        logout(request)
        return redirect('home')
    

def check_view(request, course_id,assignment_id):
    if is_teacher(request.user.id):
        assignment_Q = Assignment_Q.objects.filter(id = assignment_id)
        assignments = Assignment_Ans.objects.filter(assignment_id = assignment_Q[0].id)
        course = Course.objects.get(id = course_id)
        student_id = []
        for assignment in assignments:
            student_id.append(assignment.student_id.all())
        student_list = []
        for student in student_id:
            for s in student:
                student_list.append(s)
        assignments_with_student = zip(assignments, student_list)
        return render(request, 'teacher/check_view.html', { 'assignments_with_student':assignments_with_student, 'course':course, 'assignment_Q_id':assignment_id })
    else:
        logout(request)
        return redirect('home')

def assignment_check(request, course_id, assignment_id, student_id):
    if is_teacher(request.user.id):
        assignment_ans = Assignment_Ans.objects.get(id = student_id)
        assignment_q = Assignment_Q.objects.filter(id = assignment_id)
        status = Status.objects.get(assignment_id = assignment_q[0])
        if request.method == "POST":
            marks_obtained = request.POST['marks_obtained']
            marks_outof = request.POST['marks_outof']
            assignment_ans.marks_obtained = marks_obtained
            assignment_ans.marks_outof = marks_outof
            assignment_ans.is_checked = True
            assignment_ans.save()
            status.check_no += 1
            status.uncheck_no = status.submitted_assignment - status.check_no
            status.save()
            url = '/teacher/course/check-view/{0}/{1}'.format(course_id, assignment_id)
            return redirect(url)
        else:
            question_list = json.loads(assignment_q[0].question_list)
            course = Course.objects.filter(id = course_id)
            ans_list = json.loads(assignment_ans.answer_list)
            ques_and_ans = zip(question_list, ans_list)
            return render(request, 'teacher/assignment_check_view.html',{ 'ques_and_ans':ques_and_ans, 'assignment':assignment_q[0], 'course':course[0], 'student_id':student_id })
    else:
        logout(request)
        return redirect('home')

def viewRemainingStudent(request, course_id, assignment_id):
    if is_teacher(request.user.id):
        list = Assignment_Ans.objects.filter(course_id = course_id, assignment_id = assignment_id)
        student_id = []
        for data in list:
            student_id.append(User.objects.get(id__in = data.student_id.all()))
        id_list = []
        for s in student_id:
            id_list.append(s.id)
        list = Student.objects.exclude(student_id__in = id_list)
        a = []
        for s in list:
            a.append(s.student_id)
        b = []
        for u in a:
            b.append(User.objects.get(id = u.id))
        assignment = Assignment_Q.objects.filter(id = assignment_id)
        course = Course.objects.filter(id = course_id) 
        return render(request, 'teacher/remaining_student.html', { 'assignment':assignment[0], 'course':course[0], 'students':b })
    else:
        logout(request)
        return redirect('home')