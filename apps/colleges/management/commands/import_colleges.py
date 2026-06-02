import csv
import os
from django.core.management.base import BaseCommand
from django.db import transaction
from apps.colleges.models import College, Course


class Command(BaseCommand):
    help = 'Import college data from CSV file'

    def add_arguments(self, parser):
        parser.add_argument(
            '--csv',
            type=str,
            default='data/College_Fees_Master_2026-27.csv',
            help='Path to the CSV file'
        )

    def handle(self, *args, **options):
        csv_path = options['csv']
        
        if not os.path.exists(csv_path):
            self.stdout.write(self.style.ERROR(f'CSV file not found: {csv_path}'))
            self.stdout.write(f'Please provide the correct path to your CSV file')
            return

        self.stdout.write(f'Importing data from: {csv_path}')
        
        # Dictionary to track colleges and their courses
        colleges_dict = {}
        courses_list = []
        
        with open(csv_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            
            for row in reader:
                college_name = row.get('College', '').strip()
                location = row.get('Location', '').strip()
                state = row.get('State', '').strip()
                program_level = row.get('Program Level', '').strip()
                specialization = row.get('Course / Specialization', '').strip()
                total_fee = row.get('Total Fee (INR)', '').strip()
                notes = row.get('Notes', '').strip()
                
                if not college_name:
                    continue
                
                # Clean up fee value
                if total_fee and total_fee.lower() != 'not listed':
                    total_fee = total_fee.replace('₹', '').replace(',', '').strip()
                
                # Create college key
                college_key = f"{college_name}|{location}|{state}"
                
                if college_key not in colleges_dict:
                    colleges_dict[college_key] = {
                        'name': college_name,
                        'location': location,
                        'state': state,
                        'description': None,
                        'website': None,
                        'established_year': None,
                        'hostel_available': False,
                        'placement_available': False,
                        'courses': []
                    }
                
                # Add course
                if program_level or specialization:
                    colleges_dict[college_key]['courses'].append({
                        'program_level': program_level,
                        'specialization': specialization,
                        'total_fee': total_fee if total_fee else 'Contact college',
                        'notes': notes
                    })
        
        self.stdout.write(f'Found {len(colleges_dict)} unique colleges')
        
        # Import data into database
        with transaction.atomic():
            # Clear existing data
            Course.objects.all().delete()
            College.objects.all().delete()
            
            college_objects = []
            course_objects = []
            
            for college_data in colleges_dict.values():
                # Create college
                college = College.objects.create(
                    name=college_data['name'],
                    location=college_data['location'],
                    state=college_data['state'],
                    hostel_available=False,  # Default
                    placement_available=False  # Default
                )
                college_objects.append(college)
                
                # Create courses
                for course_data in college_data['courses']:
                    course = Course(
                        college=college,
                        program_level=course_data['program_level'],
                        specialization=course_data['specialization'],
                        total_fee=course_data['total_fee'],
                        notes=course_data['notes']
                    )
                    course_objects.append(course)
            
            # Bulk create courses
            Course.objects.bulk_create(course_objects)
            
            total_courses = len(course_objects)
        
        self.stdout.write(self.style.SUCCESS(
            f'Successfully imported {len(college_objects)} colleges and {total_courses} courses'
        ))
        
        # Print summary
        self.stdout.write('\n--- Import Summary ---')
        self.stdout.write(f'States: {College.objects.values_list("state", flat=True).distinct().count()} unique states')
        self.stdout.write(f'Locations: {College.objects.values_list("location", flat=True).distinct().count()} unique locations')
        self.stdout.write(f'Program Levels: {Course.objects.values_list("program_level", flat=True).distinct().count()} unique program levels')