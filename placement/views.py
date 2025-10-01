from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.http import HttpResponseNotAllowed
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.db.models import Avg, Count
from django.db import IntegrityError
import json
from .models import Student, Company, JobPosting, Internship, Placement, JobApplication, InternshipApplication
from rest_framework import generics
from .models import JobPosting, Internship, Student
from .serializers import JobPostingSerializer, InternshipSerializer, StudentSerializer
def home(request):
    
    return render(request, 'home.html', {
        'total_students': Student.objects.count(),
        'total_companies': Company.objects.count(),
        'active_jobs': JobPosting.objects.count(),
        'active_internships': Internship.objects.count(),
    })

def dashboard(request):
    total_students = Student.objects.count()
    total_placements = Placement.objects.count()
    total_companies = Company.objects.count()
    active_jobs = JobPosting.objects.count()
    active_internships = Internship.objects.count()
    
    highest_package_obj = Placement.objects.order_by('-package').first()
    highest_package = highest_package_obj.package if highest_package_obj else 0
    
    avg_package_result = Placement.objects.aggregate(avg_package=Avg('package'))
    avg_package = avg_package_result['avg_package'] if avg_package_result['avg_package'] else 0
    
    placement_percentage = int((total_placements / total_students) * 100) if total_students > 0 else 0

    # DYNAMIC DATA FOR CHARTS
    # Course-wise placement data for pie chart
    course_placement_data = []
    if total_placements > 0:
        course_stats = Placement.objects.values('student__course').annotate(count=Count('student')).order_by('student__course')
        for stat in course_stats:
            course_placement_data.append({
                'course': stat['student__course'],
                'count': stat['count']
            })
    else:
        # Show sample data if no placements exist
        course_placement_data = [
            {'course': 'B.Tech CSE', 'count': 0},
            {'course': 'B.Tech IT', 'count': 0},
            {'course': 'BCA', 'count': 0},
            {'course': 'B.Tech ME', 'count': 0}
        ]

    # Package distribution data for bar chart
    package_distribution = []
    if total_placements > 0:
        ranges = [
            (0, 5, '0-5 LPA'),
            (5, 10, '5-10 LPA'),
            (10, 15, '10-15 LPA'),
            (15, 100, '15+ LPA')
        ]
        
        for min_pkg, max_pkg, label in ranges:
            if max_pkg == 100:
                count = Placement.objects.filter(package__gte=min_pkg).count()
            else:
                count = Placement.objects.filter(package__gte=min_pkg, package__lt=max_pkg).count()
            package_distribution.append({
                'range': label,
                'count': count
            })
    else:
        # Show empty data if no placements exist
        package_distribution = [
            {'range': '0-5 LPA', 'count': 0},
            {'range': '5-10 LPA', 'count': 0},
            {'range': '10-15 LPA', 'count': 0},
            {'range': '15+ LPA', 'count': 0}
        ]

    return render(request, 'dashboard.html', {
        'total_students': total_students,
        'placed_students': total_placements,
        'highest_package': highest_package,
        'avg_package': round(avg_package, 1) if avg_package else 0,
        'total_companies': total_companies,
        'placement_percentage': placement_percentage,
        'active_jobs': active_jobs,
        'active_internships': active_internships,
        'course_placement_data': json.dumps(course_placement_data),
        'package_distribution': json.dumps(package_distribution),
    })

@staff_member_required
def students_list(request):
    students = Student.objects.all()
    search = request.GET.get('search')
    if search:
        students = students.filter(name__icontains=search)
    paginator = Paginator(students, 10)
    page_number = request.GET.get('page')
    students = paginator.get_page(page_number)
    return render(request, 'students_list.html', {
        'students': students,
        'search': search or "",
    })

def companies_list(request):
    companies = Company.objects.all().order_by('name')
    return render(request, 'companies_list.html', {'companies': companies})

def job_postings_list(request):
    jobs = JobPosting.objects.all()
    return render(request, 'job_postings_list.html', {'jobs': jobs})

def internships_list(request):
    internships = Internship.objects.all()
    return render(request, 'internships_list.html', {'internships': internships})

def placements_list(request):
    placements = Placement.objects.select_related('student', 'company').all()
    return render(request, 'placements_list.html', {'placements': placements})

@login_required
def apply_for_job(request, job_id):
    job = get_object_or_404(JobPosting, pk=job_id)
    try:
        student = Student.objects.get(user=request.user)
    except Student.DoesNotExist:
        messages.error(request, 'Student profile not found. Please contact the admin.')
        return redirect('placement:job_postings_list')

    if JobApplication.objects.filter(student=student, job=job).exists():
        messages.warning(request, f'You have already applied for {job.title} at {job.company.name}!')
        return redirect('placement:job_postings_list')

    if request.method == "POST":
        cover_letter = request.POST.get('cover_letter', '')
        
        try:
            JobApplication.objects.create(
                student=student,
                job=job,
                cover_letter=cover_letter
            )
            messages.success(request, f"Successfully applied for {job.title} at {job.company.name}!")
            return redirect('placement:job_postings_list')
        except IntegrityError:
            messages.error(request, 'Application already exists!')
            return redirect('placement:job_postings_list')

    return render(request, 'apply_job.html', {'job': job, 'student': student})

@login_required
def apply_for_internship(request, internship_id):
    internship = get_object_or_404(Internship, pk=internship_id)
    try:
        student = Student.objects.get(user=request.user)
    except Student.DoesNotExist:
        messages.error(request, 'Student profile not found. Please contact the admin.')
        return redirect('placement:internships_list')

    if InternshipApplication.objects.filter(student=student, internship=internship).exists():
        messages.warning(request, f'You have already applied for {internship.title} at {internship.company.name}!')
        return redirect('placement:internships_list')

    if request.method == "POST":
        cover_letter = request.POST.get('cover_letter', '')
        
        try:
            InternshipApplication.objects.create(
                student=student,
                internship=internship,
                cover_letter=cover_letter
            )
            messages.success(request, f"Successfully applied for {internship.title} at {internship.company.name}!")
            return redirect('placement:internships_list')
        except IntegrityError:
            messages.error(request, 'Application already exists!')
            return redirect('placement:internships_list')

    return render(request, 'apply_internship.html', {'internship': internship, 'student': student})

def student_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome back, {user.first_name or user.username}!")
            return redirect('placement:student_dashboard')
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'student_login.html')

@login_required
def student_logout(request):
    if request.method not in ['POST', 'GET']:
        return HttpResponseNotAllowed(['POST', 'GET'])
    user_name = request.user.first_name or request.user.username
    logout(request)
    messages.success(request, f"Successfully logged out. See you soon, {user_name}!")
    return redirect('placement:home')

def student_register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered.')
        else:
            user = User.objects.create_user(
                username=username, 
                email=email, 
                password=password,
                first_name=first_name, 
                last_name=last_name
            )
            messages.success(request, 'Account created successfully! Please log in.')
            return redirect('placement:student_login')
    return render(request, 'student_register.html')

@login_required
def student_dashboard(request):
    try:
        student = Student.objects.get(user=request.user)
        
        job_applications = JobApplication.objects.filter(student=student).count()
        internship_applications = InternshipApplication.objects.filter(student=student).count()
        total_applications = job_applications + internship_applications
        
        interviews_count = JobApplication.objects.filter(
            student=student, 
            status__in=['shortlisted', 'interviewed']
        ).count() + InternshipApplication.objects.filter(
            student=student, 
            status__in=['shortlisted', 'interviewed']
        ).count()
        
        placement = Placement.objects.filter(student=student).first()
        
        context = {
            'student': student,
            'applications': total_applications,
            'interviews': interviews_count,
            'job_applications': job_applications,
            'internship_applications': internship_applications,
            'placement': placement,
            'is_placed': placement is not None,
        }
    except Student.DoesNotExist:
        messages.error(request, 'Student profile not found. Please contact the admin to create your profile.')
        context = {'student': None}
    
    return render(request, 'student_dashboard.html', context)

class JobPostingListAPIView(generics.ListAPIView):
    queryset = JobPosting.objects.all()
    serializer_class = JobPostingSerializer

class InternshipListAPIView(generics.ListAPIView):
    queryset = Internship.objects.all()
    serializer_class = InternshipSerializer

class StudentListAPIView(generics.ListAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer