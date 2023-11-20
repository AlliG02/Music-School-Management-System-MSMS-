"""Create functions for HTTP requests of URL's in the app"""
from django.contrib import messages
from django.shortcuts import redirect, render
from .forms import SignUpForm, LogInForm, requestLessonForm
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from lessons.tests.helpers import LogInTester
from .helpers import already_logged_in

@already_logged_in
def greet(request):
    return render(request, 'greet.html')

@already_logged_in
def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        #if form data provided by user is valid
        if form.is_valid():
            student = form.save()
            login(request, student)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'sign_up.html', {'form': form})

@already_logged_in
def log_in(request):
    if request.method == 'POST':
        form = LogInForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            student = authenticate(username=username, password=password)
            if student is not None:
                login(request, student)
                redirect_url = request.POST.get('next') or 'home'
                return redirect(redirect_url)
        #in the case the user is not redirected, provides the reason that details were incorrect
        messages.add_message(request, messages.ERROR, 'Incorrect Details Provided')
    form = LogInForm()
    next = request.GET.get('next') or ''
    return render(request, 'log_in.html', {'form':form, 'next': next})

def log_out(request):
    logout(request)
    return redirect('greet')

@login_required
def home(request):
    return render(request, 'home.html')

@login_required
def requestLesson(request):
    if request.method == 'POST':
        form = requestLessonForm(request.POST)
        #if form data provided by user is valid
        if form.is_valid():
            request = form.save()
            return redirect('successfulRequest')
    else:
        form = requestLessonForm()
    return render(request, 'request_lesson.html', {'form': form})

@login_required
def successfulRequest(request):
    return render(request, 'successful_request.html')

@login_required
def myRequests(request):
    return render(request, 'my_requests.html')
