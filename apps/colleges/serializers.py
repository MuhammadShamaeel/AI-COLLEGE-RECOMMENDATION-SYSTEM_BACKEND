from rest_framework import serializers

from .models import College, Course


# ============================================================
# COURSE SERIALIZER
# ============================================================

class CourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course

        fields = [
            "id",
            "program_level",
            "specialization",
            "total_fee",
            "notes",
        ]


# ============================================================
# COLLEGE LIST SERIALIZER  (used in list/search views)
# ============================================================

class CollegeListSerializer(serializers.ModelSerializer):

    class Meta:
        model = College

        fields = [
            "id",
            "name",
            "location",
            "state",
            "hostel_available",
            "placement_available",
        ]


# ============================================================
# COLLEGE DETAIL SERIALIZER  (used in detail view)
# ============================================================

class CollegeDetailSerializer(serializers.ModelSerializer):

    courses = CourseSerializer(many=True, read_only=True)

    class Meta:
        model = College

        fields = [
            "id",
            "name",
            "location",
            "state",
            "description",
            "website",
            "established_year",
            "hostel_available",
            "placement_available",
            "courses",
            "created_at",
        ]