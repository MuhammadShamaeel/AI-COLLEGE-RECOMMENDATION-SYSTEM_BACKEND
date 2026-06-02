from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.db.models import Q
import re

from .models import College, Course
from .serializers import CollegeListSerializer, CollegeDetailSerializer, CourseSerializer


def extract_numeric_fee(fee_string):
    """Extract numeric value from fee string (e.g., '3,00,000' -> 300000)"""
    if not fee_string:
        return None
    numbers = re.findall(r'[\d,]+', str(fee_string))
    if numbers:
        cleaned = numbers[0].replace(',', '')
        try:
            return int(cleaned)
        except ValueError:
            return None
    return None


# ============================================================
# COLLEGE LIST & SEARCH VIEW - PUBLIC
# GET /api/colleges/
# ============================================================

class CollegeListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        print("=" * 50)
        print("COLLEGE LIST VIEW CALLED")
        print(f"Query params: {request.query_params}")
        
        # Get filter parameters
        state = request.query_params.get("state", "").strip()
        location = request.query_params.get("location", "").strip()
        program_level = request.query_params.get("program_level", "").strip()
        course = request.query_params.get("course", "").strip()
        search = request.query_params.get("search", "").strip()
        
        # Start with all colleges
        colleges = College.objects.all()
        
        # First, find colleges that have matching courses
        college_ids_with_matching_courses = set()
        
        if course or program_level:
            # Filter courses first
            filtered_courses = Course.objects.all()
            
            if course:
                filtered_courses = filtered_courses.filter(
                    Q(specialization__icontains=course) |
                    Q(program_level__icontains=course)
                )
                print(f"Courses matching '{course}': {filtered_courses.count()}")
            
            if program_level:
                filtered_courses = filtered_courses.filter(
                    program_level__icontains=program_level
                )
                print(f"Courses matching program_level '{program_level}': {filtered_courses.count()}")
            
            # Get unique college IDs from matching courses
            college_ids_with_matching_courses = set(filtered_courses.values_list('college_id', flat=True))
            print(f"Colleges with matching courses: {len(college_ids_with_matching_courses)}")
            
            # Filter colleges to only those with matching courses
            colleges = colleges.filter(id__in=college_ids_with_matching_courses)
        
        # Apply state filter
        if state:
            print(f"Filtering by state: {state}")
            colleges = colleges.filter(state__icontains=state)
            print(f"After state filter: {colleges.count()}")
        
        # Apply location filter
        if location:
            print(f"Filtering by location: {location}")
            colleges = colleges.filter(location__icontains=location)
            print(f"After location filter: {colleges.count()}")
        
        # Apply search filter (college name)
        if search:
            colleges = colleges.filter(name__icontains=search)
        
        # Prepare result with filtered courses only
        result = []
        for college in colleges:
            # Get courses for this college that match the filters
            college_courses = Course.objects.filter(college=college)
            
            if course:
                college_courses = college_courses.filter(
                    Q(specialization__icontains=course) |
                    Q(program_level__icontains=course)
                )
            
            if program_level and not course:
                college_courses = college_courses.filter(
                    program_level__icontains=program_level
                )
            
            if not college_courses.exists():
                continue
            
            # Calculate min fee from matching courses only
            min_fee = None
            for c in college_courses:
                fee_num = extract_numeric_fee(c.total_fee)
                if fee_num and (min_fee is None or fee_num < min_fee):
                    min_fee = fee_num
            
            result.append({
                "id": college.id,
                "name": college.name,
                "location": college.location,
                "state": college.state,
                "hostel_available": college.hostel_available,
                "placement_available": college.placement_available,
                "courses": [
                    {
                        "id": c.id,
                        "program_level": c.program_level,
                        "specialization": c.specialization,
                        "total_fee": c.total_fee,
                        "notes": c.notes
                    } for c in college_courses
                ],
                "matching_courses_count": college_courses.count(),
                "min_fee_numeric": min_fee
            })
        
        # Apply sorting
        sort_by = request.query_params.get("sort_by", "fee_asc")
        if sort_by == "fee_asc":
            result.sort(key=lambda x: x.get('min_fee_numeric') or float('inf'))
        elif sort_by == "fee_desc":
            result.sort(key=lambda x: x.get('min_fee_numeric') or float('inf'), reverse=True)
        elif sort_by == "name_asc":
            result.sort(key=lambda x: x.get('name', ''))
        elif sort_by == "name_desc":
            result.sort(key=lambda x: x.get('name', ''), reverse=True)
        
        print(f"Final result count: {len(result)}")
        print("=" * 50)
        
        return Response({
            "success": True,
            "count": len(result),
            "data": result,
            "filters_applied": {
                "state": state,
                "location": location,
                "program_level": program_level,
                "course": course,
                "sort_by": sort_by
            }
        })


# ============================================================
# COLLEGE DETAIL VIEW - PUBLIC
# GET /api/colleges/<id>/
# ============================================================

class CollegeDetailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, pk):
        try:
            college = College.objects.get(pk=pk)
        except College.DoesNotExist:
            return Response(
                {"success": False, "message": "College not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        
        courses = Course.objects.filter(college=college)
        
        data = {
            "id": college.id,
            "name": college.name,
            "location": college.location,
            "state": college.state,
            "description": college.description,
            "website": college.website,
            "established_year": college.established_year,
            "hostel_available": college.hostel_available,
            "placement_available": college.placement_available,
            "courses": [
                {
                    "id": c.id,
                    "program_level": c.program_level,
                    "specialization": c.specialization,
                    "total_fee": c.total_fee,
                    "notes": c.notes
                } for c in courses
            ]
        }
        
        return Response({"success": True, "data": data})


# ============================================================
# COLLEGE COURSE LIST VIEW - PUBLIC
# GET /api/colleges/<id>/courses/
# ============================================================

class CollegeCourseListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, pk):
        try:
            college = College.objects.get(pk=pk)
        except College.DoesNotExist:
            return Response(
                {"success": False, "message": "College not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        
        courses = Course.objects.filter(college=college)
        
        program_level = request.query_params.get("program_level")
        if program_level:
            courses = courses.filter(program_level__icontains=program_level)
        
        serializer = CourseSerializer(courses, many=True)
        
        return Response({
            "success": True,
            "college": college.name,
            "count": courses.count(),
            "data": serializer.data
        })


# ============================================================
# COLLEGE FILTER OPTIONS VIEW - PUBLIC
# GET /api/colleges/filters/
# ============================================================

class CollegeFilterOptionsView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        print("=" * 50)
        print("FILTER OPTIONS VIEW CALLED")
        
        # Get unique states
        states = College.objects.values_list('state', flat=True).distinct()
        states = sorted(list(set([s for s in states if s and s.strip()])))
        print(f"States found: {states}")
        
        # Get unique locations
        locations = College.objects.values_list('location', flat=True).distinct()
        locations = sorted(list(set([l for l in locations if l and l.strip()])))[:50]
        print(f"Locations found: {len(locations)}")
        
        # Get unique program levels
        program_levels = Course.objects.values_list('program_level', flat=True).distinct()
        program_levels = sorted(list(set([p for p in program_levels if p and p.strip()])))[:30]
        print(f"Program levels found: {len(program_levels)}")
        
        print("=" * 50)
        
        return Response({
            "success": True,
            "data": {
                "states": states,
                "locations": locations,
                "program_levels": program_levels,
                "specializations": []
            }
        })