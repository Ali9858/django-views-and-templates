
from django.urls import path
from . import views

app_name = 'onlinecourse'

urlpatterns = [
    path(
        '',
        views.CourseListView.as_view(),
        name='popular_course_list'
    ),

    path(
        'course/<int:pk>/enroll/',
        views.EnrollView.as_view(),
        name='enroll'
    ),

    path(
        'course/<int:pk>/',
        views.CourseDetailsView.as_view(),
        name='course_details'
    ),
]


