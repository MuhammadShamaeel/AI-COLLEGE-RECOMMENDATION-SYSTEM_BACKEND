from django.contrib import admin

from .models import College, Course


# ============================================================
# COURSE INLINE  (shown inside College admin page)
# ============================================================

class CourseInline(admin.TabularInline):

    model = Course

    extra = 0

    fields = [
        "program_level",
        "specialization",
        "total_fee",
        "notes",
    ]


# ============================================================
# COLLEGE ADMIN
# ============================================================

@admin.register(College)
class CollegeAdmin(admin.ModelAdmin):

    list_display = [
        "name",
        "location",
        "state",
        "hostel_available",
        "placement_available",
        "created_at",
    ]

    list_filter = [
        "state",
        "hostel_available",
        "placement_available",
    ]

    search_fields = [
        "name",
        "location",
    ]

    inlines = [CourseInline]


# ============================================================
# COURSE ADMIN
# ============================================================

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):

    list_display = [
        "specialization",
        "program_level",
        "total_fee",
        "college",
    ]

    list_filter = [
        "program_level",
        "college__state",
    ]

    search_fields = [
        "specialization",
        "college__name",
    ]