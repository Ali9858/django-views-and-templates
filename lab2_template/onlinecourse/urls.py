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
        'course/<int:pk>/',
        views.CourseDetailsView.as_view(),
        name='course_details'
    ),

    path(
        'course/<int:pk>/enroll/',
        views.EnrollView.as_view(),
        name='enroll'
    ),

    path(
        'login/',
        views.login_request,
        name='login'
    ),

    path(
        'logout/',
        views.logout_request,
        name='logout'
    ),

    path(
        'registration/',
        views.registration_request,
        name='registration'
    ),

    path(
        '<int:course_id>/submit/',
        views.submit,
        name='submit'
    ),

    path(
        'course/<int:course_id>/submission/<int:submission_id>/result/',
        views.show_exam_result,
        name='exam_result'
    ),
]


