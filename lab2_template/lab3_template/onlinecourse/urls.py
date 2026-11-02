
from django.urls import path
from . import views

app_name = 'onlinecourse'

urlpatterns = [
    path(
        '',
        views.popular_course_list,
        name='popular_course_list'
    ),

    path(
        'course/<int:course_id>/enroll/',
        views.enroll,
        name='enroll'
    ),

    path(
        'course/<int:course_id>/',
        views.course_details,
        name='course_details'
    ),
]


