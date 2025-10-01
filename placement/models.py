from django.db import models
from django.contrib.auth.models import User
import os

def resume_upload_path(instance, filename):
    return os.path.join('resumes', f'student_{instance.id or "new"}', filename)

class Student(models.Model):
    COURSE_CHOICES = [
        ('B.Tech CSE', 'B.Tech Computer Science Engineering'),
        ('B.Tech IT', 'B.Tech Information Technology'),
        ('B.Tech ECE', 'B.Tech Electronics & Communication'),
        ('B.Tech ME', 'B.Tech Mechanical Engineering'),
        ('B.Tech CE', 'B.Tech Civil Engineering'),
        ('B.Tech EE', 'B.Tech Electrical Engineering'),
        ('BCA', 'Bachelor of Computer Applications'),
        ('MCA', 'Master of Computer Applications'),
        ('MBA', 'Master of Business Administration'),
        ('B.Sc CS', 'B.Sc Computer Science'),
        ('M.Tech', 'Master of Technology'),
        ('Other', 'Other'),
    ]
    
    YEAR_CHOICES = [
        ('1st', '1st Year'),
        ('2nd', '2nd Year'),
        ('3rd', '3rd Year'),
        ('4th', '4th Year'),
        ('Final', 'Final Year'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    enrollment_no = models.CharField(max_length=20, unique=True)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    course = models.CharField(max_length=100, choices=COURSE_CHOICES, default='B.Tech CSE')
    year = models.CharField(max_length=10, choices=YEAR_CHOICES, default='1st')
    cgpa = models.FloatField()
    skills = models.TextField(blank=True, default='')  # Fix: Make it not required
    resume = models.FileField(upload_to=resume_upload_path, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Company(models.Model):
    name = models.CharField(max_length=200)
    industry = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15, blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    INDUSTRY_CHOICES = [
        ('IT', 'Information Technology'),
        ('Service', 'Service'),
        ('Finance', 'Finance'),
        ('Edu', 'Education'),
        ('Manufacturing', 'Manufacturing'),
        ('Healthcare', 'Healthcare'),
        ('Sales', 'Sales'),
        ('Marketing', 'Marketing'),
        ('HR', 'Human Resources'),
        ('Others', 'Others'),
    ]
    name = models.CharField(max_length=200)
    industry = models.CharField(max_length=50, choices=INDUSTRY_CHOICES, default='IT')
    def __str__(self):
        return self.name

class JobPosting(models.Model):
    title = models.CharField(max_length=200)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='job_postings')
    description = models.TextField()
    requirements = models.TextField()
    responsibilities = models.TextField()
    location = models.CharField(max_length=100)
    package_min = models.FloatField()
    package_max = models.FloatField()
    positions_available = models.IntegerField()
    application_deadline = models.DateField()
    posted_on = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='active')
    eligible_courses = models.TextField()

    def __str__(self):
        return f"{self.title} - {self.company.name}"

class Internship(models.Model):
    title = models.CharField(max_length=200)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='internships')
    description = models.TextField()
    location = models.CharField(max_length=100)
    stipend = models.FloatField()
    duration = models.CharField(max_length=50)
    start_date = models.DateField()
    end_date = models.DateField()
    positions_available = models.IntegerField()
    application_deadline = models.DateField()
    posted_on = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='active')
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('closed', 'Closed'),
    ]
    # other fields...
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')

    def __str__(self):
        return f"{self.title} - {self.company.name}"

class Placement(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    job_role = models.CharField(max_length=200)
    package = models.FloatField()
    location = models.CharField(max_length=100)
    joining_date = models.DateField()
    placed_on = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.name} - {self.company.name}"

class JobApplication(models.Model):
    STATUS_CHOICES = [
        ('applied', 'Applied'),
        ('shortlisted', 'Shortlisted'),
        ('interviewed', 'Interviewed'),
        ('selected', 'Selected'),
        ('rejected', 'Rejected'),
    ]
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='job_applications')
    job = models.ForeignKey(JobPosting, on_delete=models.CASCADE, related_name='applications')
    applied_on = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='applied')
    cover_letter = models.TextField(blank=True, null=True)
    
    class Meta:
        unique_together = ['student', 'job']
    
    def __str__(self):
        return f"{self.student.name} - {self.job.title}"

class InternshipApplication(models.Model):
    STATUS_CHOICES = [
        ('applied', 'Applied'),
        ('shortlisted', 'Shortlisted'),
        ('interviewed', 'Interviewed'),
        ('selected', 'Selected'),
        ('rejected', 'Rejected'),
    ]
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='internship_applications')
    internship = models.ForeignKey(Internship, on_delete=models.CASCADE, related_name='applications')
    applied_on = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='applied')
    cover_letter = models.TextField(blank=True, null=True)
    
    class Meta:
        unique_together = ['student', 'internship']
    
    def __str__(self):
        return f"{self.student.name} - {self.internship.title}"
