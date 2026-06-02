from django.urls import path
from .views import (
    CollegeListView,
    CollegeDetailView,
    CollegeCourseListView,
    CollegeFilterOptionsView,
)

urlpatterns = [
    path("", CollegeListView.as_view(), name="college-list"),
    path("filters/", CollegeFilterOptionsView.as_view(), name="college-filters"),
    path("<int:pk>/", CollegeDetailView.as_view(), name="college-detail"),
    path("<int:pk>/courses/", CollegeCourseListView.as_view(), name="college-courses"),
]