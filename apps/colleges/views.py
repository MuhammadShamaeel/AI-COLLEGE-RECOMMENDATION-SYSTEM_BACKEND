from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

from .models import College, Course
from .serializers import CollegeListSerializer, CollegeDetailSerializer, CourseSerializer


# ============================================================
# COLLEGE LIST & SEARCH VIEW
# GET /api/colleges/
# GET /api/colleges/?course=CSE&location=Kerala&state=Kerala
# ============================================================

class CollegeListView(APIView):

    permission_classes = [AllowAny]

    def get(self, request):

        colleges = College.objects.all()

        # Optional filters from query params
        course   = request.query_params.get("course")
        location = request.query_params.get("location")
        state    = request.query_params.get("state")

        if course:
            colleges = colleges.filter(
                courses__specialization__icontains=course
            ).distinct()

        if location:
            colleges = colleges.filter(
                location__icontains=location
            )

        if state:
            colleges = colleges.filter(
                state__icontains=state
            )

        serializer = CollegeListSerializer(colleges, many=True)

        return Response(
            {
                "success": True,
                "count": colleges.count(),
                "data": serializer.data,
            }
        )


# ============================================================
# COLLEGE DETAIL VIEW
# GET /api/colleges/<id>/
# ============================================================

class CollegeDetailView(APIView):

    permission_classes = [AllowAny]

    def get(self, request, pk):

        try:
            college = College.objects.get(pk=pk)

        except College.DoesNotExist:
            return Response(
                {
                    "success": False,
                    "message": "College not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = CollegeDetailSerializer(college)

        return Response(
            {
                "success": True,
                "data": serializer.data,
            }
        )


# ============================================================
# COURSES BY COLLEGE VIEW
# GET /api/colleges/<id>/courses/
# ============================================================

class CollegeCourseListView(APIView):

    permission_classes = [AllowAny]

    def get(self, request, pk):

        try:
            college = College.objects.get(pk=pk)

        except College.DoesNotExist:
            return Response(
                {
                    "success": False,
                    "message": "College not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        courses = Course.objects.filter(college=college)

        # Optional filter by program level
        program_level = request.query_params.get("program_level")

        if program_level:
            courses = courses.filter(
                program_level__icontains=program_level
            )

        serializer = CourseSerializer(courses, many=True)

        return Response(
            {
                "success": True,
                "college": college.name,
                "count": courses.count(),
                "data": serializer.data,
            }
        )