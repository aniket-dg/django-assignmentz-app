from django.urls import path
from .views import dashboard, getProfile, course, create_assignment, assignment_submit, assignment_view, check_view, assignment_check
from .views import viewRemainingStudent
app_name = "teacher"
urlpatterns = [
    path('dashboard', dashboard, name='dashboard'),
    path('', dashboard, name='dashboard'),
    path('profile', getProfile, name='profile'),
    path('course/<id>', course, name='course'),

    path('course/create-assignment/<id>', create_assignment, name="create_assignment"),
    path('course/create-assignment/<id>/assignment-submit', assignment_submit, name='assignment_submit'),
    path('course/view-assignment/<course_id>/<assignment_id>/assignment-view', assignment_view, name='assignment_view'),

    path('course/check-view/<course_id>/<assignment_id>', check_view, name="check_view"),
    path('course/view-assignment/<course_id>/<assignment_id>/<student_id>/assignment-check-view', assignment_check, name='assignment_check'),
    
    path('course/<course_id>/remaining-student/<assignment_id>/list', viewRemainingStudent, name="viewRemainingStudent"),
]