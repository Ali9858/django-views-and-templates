
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic, View

from .models import Course


# Generic View: list of popular courses
class CourseListView(generic.ListView):

    template_name = 'onlinecourse/course_list.html'
    context_object_name = 'course_list'

    def get_queryset(self):
        return Course.objects.order_by(
            '-total_enrollment'
        )[:10]


# Class-Based View: enroll in course
class EnrollView(View):

    def post(self, request, *args, **kwargs):

        course_id = kwargs.get('pk')

        course = get_object_or_404(
            Course,
            pk=course_id
        )

        course.total_enrollment += 1
        course.save()

        return HttpResponseRedirect(
            reverse(
                'onlinecourse:course_details',
                args=(course.id,)
            )
        )


# Generic View: course details
class CourseDetailsView(generic.DetailView):

    model = Course
    template_name = 'onlinecourse/course_detail.html'
