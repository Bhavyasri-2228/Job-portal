from django import forms
from .models import JobPost, Application

# Form to create a new Job Post
class JobPostForm(forms.ModelForm):
    class Meta:
        model = JobPost
        fields = ['title', 'description', 'location', 'salary']

# Form to apply for a job
class ApplicationForm(forms.ModelForm):
    dob = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))  # Better date picker

    class Meta:
        model = Application
        fields = [
            'first_name', 'last_name', 'phone', 'country_code', 'gender', 'dob',
            'education', 'experience', 'color', 'disability', 'resume'
        ]
        widgets = {
            'gender': forms.Select(choices=[
                ('Male', 'Male'),
                ('Female', 'Female'),
                ('Other', 'Other'),
            ]),
        }