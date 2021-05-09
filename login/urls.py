from django.urls import path
from .views import login_student, logout_user, change_password, change_password_view, home, login_teacher
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', home, name='home'),
    path('login/login_student',login_student,name="login_student"),
    path('login/login_teacher',login_teacher,name="login_teacher"),
    
    path('login/logout_user',logout_user,name='logout_user'),
    
    ###   Password Related Urls
    path('login/change_password_view', change_password_view, name='change_password_view'),
    path('login/change_password', change_password, name='change_password'),
    
    
    path('login/password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='login/password_reset.html'
         ),
         name='password_reset'),

    path('login/password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='login/password_reset_done.html'
         ),
         name='password_reset_done'),

    path('login/password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='login/password_reset_confirm.html'
         ),
         name='password_reset_confirm'),

    path('login/password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='login/password_reset_complete.html'
         ),
         name='password_reset_complete'),
    ### Email Send
    
]