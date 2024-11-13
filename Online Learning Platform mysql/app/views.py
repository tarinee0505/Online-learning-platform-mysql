from django.http import Http404, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .models import *
from .forms import *

def course_list(request):
    """Display all available courses"""
    courses = Course.objects.filter(is_active=True)
    return render(request, 'course_list.html', {'courses': courses})

@login_required
def course_detail(request, course_id):
    """Display detailed information about a specific course"""
    course = get_object_or_404(Course, id=course_id)
    enrollment_form = CourseEnrollForm()
    user_courses = Enrollment.objects.filter(user=request.user).values_list('course_id', flat=True)
    
    if request.method == 'POST':
        enrollment_form = CourseEnrollForm(request.POST)
        if enrollment_form.is_valid():
            Enrollment.objects.get_or_create(
                user=request.user,
                course=course
            )
            modules = Module.objects.filter(course=course)
            for module in modules:
                Progress.objects.create(
                    module=module,
                    user=request.user
                )
            messages.success(request, 'Successfully enrolled in the course!')
            return redirect('course_content', course_id=course.id)
            
    return render(request, 'course_detail.html', {
        'course': course,
        'enrollment_form': enrollment_form,
        'user_courses':user_courses
    })

@login_required
def course_content(request, course_id):
    """Display course content for enrolled users"""
    course = get_object_or_404(Course, id=course_id)
    enrollment = get_object_or_404(Enrollment, user=request.user, course=course)
    modules = Module.objects.filter(course=course).order_by('order')
    progress = Progress.objects.filter(module__in=modules,user=request.user)

    return render(request, 'course_content.html', {
        'course': course,
        'modules': modules,
        'enrollment': enrollment,
        'progress':progress
    })

@login_required
def update_progress(request, module_id):
    """Update user's progress in a module"""
    if request.method == 'POST':
        module = get_object_or_404(Module, id=module_id)
        progress, created = Progress.objects.get_or_create(
            user=request.user,
            module=module
        )
        progress.completed = True
        progress.save()
        messages.success(request, 'Progress updated successfully!')
        
    return redirect('course_content', course_id=module.course.id)

def home(request):
    featured_courses = Course.objects.filter(is_active=True, is_featured=True)[:3]
    return render(request, 'home.html', {
        'featured_courses': featured_courses
    })

@login_required
def my_courses(request):
    """Display courses that the user is enrolled in"""
    enrolled_courses = Enrollment.objects.filter(user=request.user)
    return render(request, 'my_courses.html', {
        'enrolled_courses': enrolled_courses
    })

@login_required
def profile(request):
    """Display user profile"""
    return render(request, 'profile.html', {
        'user': request.user
    })

def register(request):
    """Handle user registration with custom form"""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Registration successful! Please log in.')
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'register.html', {
        'form': form
    })

# Optional: Custom login redirect
@login_required
def login_success(request):
    """Redirect users after login based on their role"""
    messages.success(request, 'Welcome back!')
    return redirect('my_courses')

def logout_view(request):
    """Handle user logout"""
    logout(request)
    messages.success(request, 'You have been successfully logged out.')
    return redirect('home')

def login_view(request):
    """Handle user login"""
    if request.user.is_authenticated:
        return redirect('home')
        
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                # Redirect to next page if specified, otherwise to my_courses
                next_page = request.GET.get('next')
                return redirect(next_page if next_page else 'home')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    
    return render(request, 'login.html', {
        'form': form,
        'title': 'Login'
    })

def course_review(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    reviews = Review.objects.filter(course=course)
    is_reviewed = reviews.filter(user=request.user).exists()

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.course = course
            review.user = request.user
            review.save()
            return redirect('course_review', course_id=course.id)
    else:
        form = ReviewForm()

    return render(request, 'course_review.html', {
        'course': course,
        'reviews': reviews,
        'form': form,
        'is_reviewed':is_reviewed
    })

def download_file(request, module_id):
    module = get_object_or_404(Module, id=module_id)
    if module.file_attachment:
        response = HttpResponse(module.file_attachment, content_type='application/octet-stream')
        response['Content-Disposition'] = f'attachment; filename="{module.file_attachment.name}"'
        return response
    raise Http404("File not found")

@login_required
def quiz_view(request, module_id):
    module = get_object_or_404(Module, id=module_id)
    questions = module.questions.all()

    if request.method == 'POST':
        for question in questions:
            answer_text = request.POST.get(f'answer_{question.id}')
            if answer_text:
                UserAnswer.objects.update_or_create(
                    user=request.user,
                    question=question,
                    defaults={'answer_text': answer_text}
                )
        return redirect('quiz_results', module_id=module.id)  # Redirect to results page

    context = {
        'module': module,
        'questions': questions,
    }
    return render(request, 'quiz_view.html', context)

@login_required
def quiz_results(request, module_id):
    module = get_object_or_404(Module, id=module_id)
    questions = module.questions.all()
    user_answers = UserAnswer.objects.filter(user=request.user, question__in=questions)

    results = []
    for question in questions:
        user_answer = user_answers.filter(question=question).first()
        results.append({
            'question': question,
            'user_answer': user_answer,
            'is_correct': user_answer.answer_text == question.correct_answer if user_answer else None
        })

    context = {
        'module': module,
        'results': results,
    }
    return render(request, 'quiz_results.html', context)

