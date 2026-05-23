from django.db import models


# ============================================================
# COLLEGE MODEL
# ============================================================

class College(models.Model):

    name = models.CharField(max_length=255)

    location = models.CharField(max_length=255)

    state = models.CharField(max_length=100)

    description = models.TextField(
        blank=True,
        null=True
    )

    website = models.URLField(
        blank=True,
        null=True
    )

    established_year = models.PositiveIntegerField(
        blank=True,
        null=True
    )

    hostel_available = models.BooleanField(default=False)

    placement_available = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} - {self.location}"


# ============================================================
# COURSE MODEL
# ============================================================

class Course(models.Model):

    college = models.ForeignKey(
        College,
        on_delete=models.CASCADE,
        related_name="courses"
    )

    program_level = models.CharField(max_length=100)

    specialization = models.CharField(max_length=255)

    total_fee = models.CharField(
        max_length=100,
        help_text="Total fee in INR (e.g. 3,00,000)"
    )

    notes = models.TextField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["program_level", "specialization"]

    def __str__(self):
        return f"{self.program_level} - {self.specialization} ({self.college.name})"