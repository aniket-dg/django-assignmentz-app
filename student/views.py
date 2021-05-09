from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from student.models import Student , Assignment_Ans
from database.models import Course
from login.views import change_password, logout_user
from django.contrib.auth.decorators import login_required
from login.views import is_teacher, is_student, is_super
from teacher.views import dashboard as teacher_dashboard
from teacher.models import Teacher, Assignment_Q, Status
from django.contrib import messages
import json
from django.contrib.auth import logout
# Create your views here.
@login_required(login_url='/login/login_student')
def dashboard(request):
    if is_teacher(request.user.id):
        return redirect('/teacher/dashboard')
    else:
        if is_student(request.user.id):
            user = getUser(request)
            course = getCourses(request)
            teacher = getTeacher(request, course)
            assignment = getAssignment(request, course)
            course = zip(course, teacher, assignment)
            return render(request, 'student/dashboard.html', {'user':user, 'course_list': course})
        else:
            logout(request)
            return redirect('home')
@login_required(login_url='/login/login_student')            
def getTeacher(request, course):
    if is_student(request.user.id):
        teacher = []
        for c in course:
            teacher.append(Teacher.objects.get(asssigned_course = c))
        id = []
        for t in teacher:
            id.append(t.teacher_id)
        details = []
        for t in id:
            details.append(User.objects.get(id = t.id))
        return details
    else:
        logout(request)
        return redirect('home')
@login_required(login_url='/login/login_student')
def getAssignment(request, course):
    if is_student(request.user.id):
        assignment = []
        for c in course:
            assignment.append(Assignment_Q.objects.filter(course_id = c).count())
        return assignment
    else:
        logout(request)
        return redirect('home')
@login_required(login_url='/login/login_student')
def getCourses(request):
    if is_teacher(request.user.id):
        return redirect('/teacher')
    else:
        if is_student(request.user.id):
            id = int(request.user.id)
            user = Student.objects.get(student_id=id)
            course = user.registerd_course.all()
            return course
        else:
            logout(request)
            return redirect('home')
@login_required(login_url='/login/login_student')
def getUser(request):
    if is_teacher(request.user.id):
        return redirect('/teacher')
    else:
        if is_student(request.user.id):
            return User.objects.get(id = request.user.id)
        else:
            logout(request)
            return redirect('home')
@login_required(login_url='/login/login_student')
def profile(request):
    if is_teacher(request.user.id):
        return redirect('/teacher')
    else:
        if is_student(request.user.id):
            user = getUser(request)
            course = getCourses(request)
            if request.method == "POST":
                if request.POST['stud_name'] != '':
                    user.first_name = request.POST['stud_name']
                    user.save()
                if request.POST['newPassword'] != '':
                    try:
                        user.set_password(request.POST['newPassword'])
                        user.save()
                        return redirect(logout_user)
                    except Exception as e:
                        return HttpResponse(e)
                messages.success(request, "Profile Updated Successfully !")
                return redirect(profile)
            else:
                return render(request, 'student/profile.html',{ 'user':user, 'course':course })
        else:
            logout(request)
            return redirect('home')


@login_required(login_url='/login/login_student')
def course(request, id):
    if is_teacher(request.user.id):
        return redirect('/teacher')
    else:
        if is_student(request.user.id):
            course = Course.objects.get(id=int(id))
            assignment_list = Assignment_Q.objects.filter(course_id = course)
            submit_status, marks, check = getMarks(request, request.user, course)
            assignment_list = zip(assignment_list, submit_status, marks, check)
            return render(request, 'student/subject.html', { 'course': course , 'assignment_list': assignment_list})
        else:
            logout(request)
            return redirect('home')
@login_required(login_url='/login/login_student')
def getMarks(request, student, course):
    if is_student(request.user.id):
        ques = Assignment_Q.objects.filter(course_id = course)
        ans = Assignment_Ans.objects.filter(student_id = student)
        marks = []
        status = []
        check = []
        for q in ques:
            ans = Assignment_Ans.objects.filter(student_id = student, assignment_id = q.id)
            if ans:
                marks.append(ans[0].marks_obtained)
                status.append(ans[0].is_submitted)
                check.append(ans[0].is_checked)
            else:
                marks.append("Not Assigned Yet!")
                status.append(False)
                check.append(False)
        return status, marks, check
    else:
        logout(request)
        return redirect('home')
    
@login_required(login_url='/login/login_student')
def submitAssignment(request, course_id, assignment_id):
    if is_student(request.user.id):
        assignment = Assignment_Q.objects.filter(id = assignment_id)
        questions = json.loads(assignment[0].question_list)
        course = Course.objects.get(id = course_id)
        try:
            assignment_a = Assignment_Ans.objects.get(student_id = request.user, course_id = course, assignment_id= assignment_id)
            is_submitted = assignment_a.is_submitted
        except:
            is_submitted = False
        if is_submitted:
            messages.warning(request, 'You already Submitted Assignment !')
            url = '/student/course/{0}'.format(course_id)
            return redirect(url)
        if request.method == "POST" and not is_submitted:
            student = User.objects.get(id = request.user.id)
            teacher = Teacher.objects.get(asssigned_course = course)
            answer_list = []
            status = Status.objects.get(teacher_id = teacher, course_id= course, assignment_id = assignment[0])
            for i in range(1, len(questions)+1):
                answer_list.append(request.POST['%s' %(i)])
            answer_list = json.dumps(answer_list)
            is_submitted = True
            answer_submission = Assignment_Ans.objects.create(assignment_id = assignment[0].id, answer_list = answer_list, is_submitted = is_submitted)
            answer_submission.save()
            answer_submission.student_id.add(student)
            answer_submission.save()
            answer_submission.course_id.add(course)
            answer_submission.save()
            status.submitted_assignment +=1
            status.save()
            submit_student = Assignment_Ans.objects.filter(assignment_id = assignment[0].id)
            remaining_student = Student.objects.exclude(id__in = submit_student).count()
            status.remaining_student -= 1
            status.save()
            messages.success(request, 'Assignment no. %i Submitted Successfully !' %(assignment[0].assignment_no))
            url = '/student/course/{0}'.format(course_id)
            return redirect(url)
        else:
            return render(request, 'student/assignment_submit.html', { 'course': course,'assignment': assignment, 'questions':questions })
    else:
        logout(request)
        return redirect('home')

def viewSubmitAssignment(request, course_id, assignment_id):
    Assignment_q = Assignment_Q.objects.get(course_id = course_id, id = assignment_id)
    question_list = json.loads(Assignment_q.question_list)
    student = User.objects.get(id = request.user.id)
    Assignment_ans = Assignment_Ans.objects.get(assignment_id = assignment_id, student_id = student)
    answer_list = json.loads(Assignment_ans.answer_list)
    assignment = zip(question_list, answer_list)
    course = Course.objects.get(id = course_id)
    return render(request, 'student/assignment_view.html', { 'assignment':assignment, 'course':course, 'assignment_q': Assignment_q })