from django.urls import path
from .views import dashboard, profile, course, submitAssignment, viewSubmitAssignment
urlpatterns = [
    path('dashboard', dashboard, name="dashboard"),
    path('', dashboard, name="dashboard"),
    path('profile', profile, name="profile"),
    path('course/<id>',course, name="specific_course"),
    path('course/<course_id>/<assignment_id>/assignment_view/', submitAssignment, name="submitAssignment"),
    path('course/<course_id>/<assignment_id>/submit-assignment', submitAssignment, name="submitAssignment"),
    path('course/<course_id>/<assignment_id>/view/submitted/Assignment', viewSubmitAssignment, name="viewSubmitAssignment"),    

]