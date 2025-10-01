from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from .models import Student, Company, Internship, Placement, InternshipApplication

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [
            'name', 'email', 'enrollment_no', 'course', 'year', 
            'skills', 'cgpa', 'phone', 'address', 'resume', 
            'linkedin_profile', 'github_profile'
        ]
        widgets = {
            'skills': forms.Textarea(attrs={'rows': 3}),
            'address': forms.Textarea(attrs={'rows': 3}),
            'cgpa': forms.NumberInput(attrs={'step': '0.01', 'min': '0', 'max': '10'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='form-group col-md-6 mb-0'),
                Column('email', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('enrollment_no', css_class='form-group col-md-4 mb-0'),
                Column('course', css_class='form-group col-md-4 mb-0'),
                Column('year', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('cgpa', css_class='form-group col-md-6 mb-0'),
                Column('phone', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            'skills',
            'address',
            Row(
                Column('linkedin_profile', css_class='form-group col-md-6 mb-0'),
                Column('github_profile', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            'resume',
            Submit('submit', 'Save Student', css_class='btn btn-primary')
        )

class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = [
            'name', 'industry', 'location', 'website', 'email', 
            'phone', 'description', 'established_year', 'employee_count'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'established_year': forms.NumberInput(attrs={'min': '1800', 'max': '2024'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='form-group col-md-8 mb-0'),
                Column('industry', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('email', css_class='form-group col-md-6 mb-0'),
                Column('phone', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('website', css_class='form-group col-md-6 mb-0'),
                Column('location', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            'description',
            Row(
                Column('established_year', css_class='form-group col-md-6 mb-0'),
                Column('employee_count', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Submit('submit', 'Save Company', css_class='btn btn-primary')
        )

class InternshipApplicationForm(forms.ModelForm):
    class Meta:
        model = InternshipApplication
        fields = ['cover_letter']
        widgets = {
            'cover_letter': forms.Textarea(attrs={
                'rows': 5, 
                'placeholder': 'Write your cover letter here...'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'cover_letter',
            Submit('submit', 'Apply for Internship', css_class='btn btn-success')
        )
