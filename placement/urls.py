from django.urls import path
from . import views
from django.urls import path
from .views import (
    JobPostingListAPIView,
    InternshipListAPIView,
    StudentListAPIView,
)


app_name = 'placement'

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    
    path('students/', views.students_list, name='students_list'),
    path('companies/', views.companies_list, name='companies_list'),
    path('jobs/', views.job_postings_list, name='job_postings_list'),
    path('internships/', views.internships_list, name='internships_list'),
    path('placements/', views.placements_list, name='placements_list'),
    
    path('apply-job/<int:job_id>/', views.apply_for_job, name='apply_for_job'),
    path('apply-internship/<int:internship_id>/', views.apply_for_internship, name='apply_for_internship'),
    
    path('student/login/', views.student_login, name='student_login'),
    path('student/logout/', views.student_logout, name='student_logout'),
    path('student/register/', views.student_register, name='student_register'),
    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),
        
    path('api/jobs/', JobPostingListAPIView.as_view(), name='job-list-api'),
    path('api/internships/', InternshipListAPIView.as_view(), name='internship-list-api'),
    path('api/students/', StudentListAPIView.as_view(), name='student-list-api'),]
