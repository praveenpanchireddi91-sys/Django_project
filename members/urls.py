from django.urls import path
from . import views
from .views import student_list

urlpatterns = [
    # path('members/', views.members, name='members'),
    path('',views.homes,name='homes'),
    path('student_signup/',views.student_signup,name='student_signup'),
    path('teacher_signup/',views.teacher_signup,name='teacher_signup'),
    path('student_login/',views.student_login,name='student_login'),
    path('student_dashboard/',views.student_dashboard,name='student_dashboard'),
    path('teacher_login/',views.teacher_login,name='teacher_login'),
    path('signup/', views.signup, name='signup'),
    path('verify_otp/', views.verify_otp, name='verify_otp'),
    path('teachersignup/', views.teachersignup, name='teachersignup'),
    path('verifyotp/', views.verifyotp, name='verifyotp'),
    path('teacherlogin/', views.teacherlogin, name='teacherlogin'),
    path('teacher_dashboard/',views.teacher_dashboard,name='teacher_dashboard'),
    path('studentlogin/', views.studentlogin, name='studentlogin'),
    # path('attendance/', views.attendance, name='attendance'),
     path('students/', views.student_list, name='student_list'),

]