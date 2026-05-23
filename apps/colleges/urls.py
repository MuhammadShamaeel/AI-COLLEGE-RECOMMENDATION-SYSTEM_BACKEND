from django.urls import path

from .views import (
    CollegeListView,
    CollegeDetailView,
    CollegeCourseListView,
)

urlpatterns = [

    # List all colleges / search colleges
    # GET /api/colleges/
    # GET /api/colleges/?course=CSE&location=Kerala
    path(
        "",
        CollegeListView.as_view(),
        name="college-list"
    ),

    # College detail
    # GET /api/colleges/1/
    path(
        "<int:pk>/",
        CollegeDetailView.as_view(),
        name="college-detail"
    ),

    # Courses of a college
    # GET /api/colleges/1/courses/
    path(
        "<int:pk>/courses/",
        CollegeCourseListView.as_view(),
        name="college-courses"
    ),
]