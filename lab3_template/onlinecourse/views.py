
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse

from .models import Course


def popular_course_list(request):
    context = {}

    if request.method == 'GET':
        course_list = Course.objects.order_by(
            '-total_enrollment'
        )[:10]

        context['course_list'] = course_list

        return render(
            request,
            'onlinecourse/course_list.html',
            context
        )


def enroll(request, course_id):
    if request.method == 'POST':
        course = get_object_or_404(Course, pk=course_id)

        course.total_enrollment += 1
        course.save()

        return HttpResponseRedirect(
            reverse(
                'onlinecourse:course_details',
                args=(course.id,)
            )
        )

    return HttpResponseRedirect(
        reverse('onlinecourse:popular_course_list')
    )


def course_details(request, course_id):
    context = {}

    if request.method == 'GET':
        try:
            course = Course.objects.get(pk=course_id)

            context['course'] = course

            return render(
                request,
                'onlinecourse/course_detail.html',
                context
            )

        except Course.DoesNotExist:
            raise Http404("No course matches the given id.")


