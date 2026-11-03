from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.urls import reverse
from django.views import generic, View
from django.contrib.auth.decorators import login_required
import logging

from .models import Course, Lesson, Enrollment, Question, Choice, Submission

logger = logging.getLogger(__name__)


# Course list view
class CourseListView(generic.ListView):
    template_name = 'onlinecourse/course_list_bootstrap.html'
    context_object_name = 'course_list'

    def get_queryset(self):
        return Course.objects.order_by('-total_enrollment')[:10]


# Course details view
class CourseDetailsView(generic.DetailView):
    model = Course
    template_name = 'onlinecourse/course_details_bootstrap.html'
    context_object_name = 'course'


# Enrollment view
class EnrollView(View):

    def post(self, request, *args, **kwargs):
        course_id = kwargs.get('pk')
        course = get_object_or_404(Course, pk=course_id)

        if request.user.is_authenticated:
            Enrollment.objects.get_or_create(
                user=request.user,
                course=course
            )

        return HttpResponseRedirect(
            reverse(
                'onlinecourse:course_details',
                args=(course.id,)
            )
        )


# Logout view
def logout_request(request):
    logout(request)
    return redirect('onlinecourse:popular_course_list')


# Login view
def login_request(request):
    context = {}

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('psw')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect('onlinecourse:popular_course_list')

        context['error'] = 'Invalid username or password'

    return render(
        request,
        'onlinecourse/user_login.html',
        context
    )


# Registration view
def registration_request(request):
    context = {}

    if request.method == 'GET':
        return render(
            request,
            'onlinecourse/user_registration.html',
            context
        )

    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('psw')
        first_name = request.POST.get('firstname')
        last_name = request.POST.get('lastname')

        if User.objects.filter(username=username).exists():
            context['error'] = 'Username already exists'
            return render(
                request,
                'onlinecourse/user_registration.html',
                context
            )

        user = User.objects.create_user(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name
        )

        login(request, user)

        return redirect('onlinecourse:popular_course_list')


# Submit exam
@login_required(login_url='/accounts/login/')
def submit(request, course_id):

    if request.method != 'POST':
        return HttpResponseRedirect(
            reverse(
                'onlinecourse:course_details',
                args=(course_id,)
            )
        )

    course = get_object_or_404(Course, pk=course_id)

    enrollment = get_object_or_404(
        Enrollment,
        user=request.user,
        course=course
    )

    submission = Submission.objects.create(
        enrollment=enrollment
    )

    selected_ids = []

    for key, value in request.POST.items():
        if key.startswith('choice_'):
            try:
                selected_ids.append(int(value))
            except (ValueError, TypeError):
                continue

    choices = Choice.objects.filter(
        id__in=selected_ids,
        question__course=course
    )

    submission.choices.set(choices)

    return HttpResponseRedirect(
        reverse(
            'onlinecourse:exam_result',
            args=(course_id, submission.id)
        )
    )


# Show exam result
@login_required(login_url='/accounts/login/')
def show_exam_result(request, course_id, submission_id):

    course = get_object_or_404(
        Course,
        pk=course_id
    )

    submission = get_object_or_404(
        Submission,
        pk=submission_id,
        enrollment__user=request.user,
        enrollment__course=course
    )

    choices = submission.choices.all()

    selected_ids = choices.values_list('id', flat=True)

    total_score = 0

    questions = course.question_set.all()

    for question in questions:

        correct_choices = set(
            question.choice_set.filter(
                is_correct=True
            ).values_list('id', flat=True)
        )

        selected_choices = set(
            choices.filter(
                question=question
            ).values_list('id', flat=True)
        )

        if correct_choices == selected_choices:
            total_score += question.grade

    context = {
        'course': course,
        'grade': total_score,
        'choices': choices,
        'selected_ids': selected_ids,
        'passed': total_score >= 80,
    }

    return render(
        request,
        'onlinecourse/exam_result_bootstrap.html',
        context
    )
