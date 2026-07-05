from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import JobPost, Application
from .forms import JobPostForm, ApplicationForm

# Home page - List all job posts with optional filtering
def job_list(request):
    jobs = JobPost.objects.all().order_by('-posted_at')

    query = request.GET.get('q')
    location = request.GET.get('location')
    min_salary = request.GET.get('min_salary')

    if query:
        jobs = jobs.filter(title__icontains=query)

    if location:
        jobs = jobs.filter(location__icontains=location)

    if min_salary:
        try:
            min_salary = int(min_salary)
            jobs = jobs.filter(salary__gte=min_salary)
        except ValueError:
            pass  # ignore invalid salary filter

    return render(request, 'job_list.html', {'jobs': jobs})

# Job detail page
def job_detail(request, job_id):
    job = get_object_or_404(JobPost, id=job_id)
    return render(request, 'job_detail.html', {'job': job})

# Recruiter: Post a new job
@login_required
def post_job(request):
    if request.method == 'POST':
        form = JobPostForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.recruiter = request.user
            job.save()
            messages.success(request, 'Job posted successfully!')
            return redirect('job_list')
    else:
        form = JobPostForm()
    return render(request, 'post_job.html', {'form': form})

# Applicant: Apply for a job with personal details form
@login_required
def apply_job(request, job_id):
    job = get_object_or_404(JobPost, id=job_id)
    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.applicant = request.user
            application.job = job
            application.save()
            messages.success(request, 'Application submitted!')
            return redirect('dashboard')
    else:
        form = ApplicationForm()
    return render(request, 'apply_job.html', {'form': form, 'job': job})

# Signup view
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

# Dashboard view: show applications by logged-in user with status
@login_required
def dashboard(request):
    applications = Application.objects.filter(applicant=request.user).select_related('job').order_by('-applied_at')
    return render(request, 'dashboard.html', {'applications': applications})
