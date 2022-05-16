from django.urls import path
from . import views
app_name = 'analytics'
urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('profile/update/<int:pk>/', views.UserUpdateView.as_view(), name='user-update'),
    path('create/teacher/', views.CreateTeacherView.as_view(), name='create-teacher'),
    path('create/student/', views.CreateStudentView.as_view(), name='create-student'),
    path('create/course/', views.CreateCourse.as_view(), name='create-course'),
    path('assign/course/', views.AssignedCourse.as_view(), name='assign-course'),
    path('assign/course/student/', views.AssignedCourseToStudent.as_view(), name='assign-course-student'),
    path('student/list/', views.StudentListView.as_view(), name='student-list'),
    path('teacher/list/', views.TeacherListView.as_view(), name='teacher-list'),
    path('course/list/', views.CourseListView.as_view(), name='course-list'),
]