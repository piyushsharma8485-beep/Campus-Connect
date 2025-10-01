from django.contrib import admin
from .models import Student, Company, JobPosting, Internship, Placement, JobApplication, InternshipApplication

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['name', 'enrollment_no', 'course', 'year', 'cgpa', 'email']
    search_fields = ['name', 'enrollment_no', 'email']
    list_filter = ['course', 'year']
    fields = ['user', 'name', 'enrollment_no', 'email', 'phone', 'course', 'year', 'cgpa', 'skills', 'resume']

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['name', 'industry', 'location', 'email']
    search_fields = ['name', 'industry', 'location']
    list_filter = ['industry']

@admin.register(JobPosting)
class JobPostingAdmin(admin.ModelAdmin):
    list_display = ['title', 'company', 'location', 'package_min', 'package_max', 'application_deadline']
    search_fields = ['title', 'company__name']
    list_filter = ['company', 'status', 'posted_on']

@admin.register(Internship)
class InternshipAdmin(admin.ModelAdmin):
    list_display = ['title', 'company', 'location', 'stipend', 'duration', 'application_deadline']
    search_fields = ['title', 'company__name']
    list_filter = ['company', 'status', 'posted_on']

@admin.register(Placement)
class PlacementAdmin(admin.ModelAdmin):
    list_display = ['student', 'company', 'job_role', 'package', 'joining_date']
    search_fields = ['student__name', 'company__name', 'job_role']
    list_filter = ['company', 'placed_on']

@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ['student', 'job', 'applied_on', 'status']
    list_filter = ['status', 'applied_on']
    search_fields = ['student__name', 'job__title']
    actions = ['mark_shortlisted', 'mark_interviewed', 'mark_selected', 'mark_rejected']

    def mark_shortlisted(self, request, queryset):
        queryset.update(status='shortlisted')
    mark_shortlisted.short_description = "Mark as Shortlisted"

    def mark_interviewed(self, request, queryset):
        queryset.update(status='interviewed')
    mark_interviewed.short_description = "Mark as Interviewed"

    def mark_selected(self, request, queryset):
        queryset.update(status='selected')
    mark_selected.short_description = "Mark as Selected"

    def mark_rejected(self, request, queryset):
        queryset.update(status='rejected')
    mark_rejected.short_description = "Mark as Rejected"

@admin.register(InternshipApplication)
class InternshipApplicationAdmin(admin.ModelAdmin):
    list_display = ['student', 'internship', 'applied_on', 'status']
    list_filter = ['status', 'applied_on']
    search_fields = ['student__name', 'internship__title']
    actions = ['mark_shortlisted', 'mark_interviewed', 'mark_selected', 'mark_rejected']

    def mark_shortlisted(self, request, queryset):
        queryset.update(status='shortlisted')
    mark_shortlisted.short_description = "Mark as Shortlisted"

    def mark_interviewed(self, request, queryset):
        queryset.update(status='interviewed')
    mark_interviewed.short_description = "Mark as Interviewed"

    def mark_selected(self, request, queryset):
        queryset.update(status='selected')
    mark_selected.short_description = "Mark as Selected"

    def mark_rejected(self, request, queryset):
        queryset.update(status='rejected')
    mark_rejected.short_description = "Mark as Rejected"
