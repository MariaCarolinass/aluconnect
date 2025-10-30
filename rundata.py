import os
import django
import csv

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.users.models import User
from apps.instructors.models import Instructor
from apps.courses.models import Course
from apps.lessons.models import Lesson
from apps.progress.models import Progress
from apps.students.models import Student
from datetime import timedelta

users_csv_path = 'data/users.csv'
instructors_csv_path = 'data/instructors.csv'
students_csv_path = 'data/students.csv'
progress_csv_path = 'data/progress.csv'
lessons_csv_path = 'data/lessons.csv'
courses_csv_path = 'data/courses.csv'

def read_csv_file(file_path):
    """Read the CSV file and send the data to the import function."""
    with open(file_path, mode='r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        data = [row for row in reader]
        model = file_path.split('/')[-1].split('.')[0]
        import_data(data, model)

def import_data(data, model):
    print(f'Importing data for model: {model}')

    for row in data:
        if model == 'users':
            username = row.get('username')
            email = row.get('email')
            role = row.get('role')
            password = row.get('password', '12345678')
            
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                role=role
            )

            print(f'User "{username}" created successfully.')
        elif model == 'instructors':
            user_id = row.get('user_id')
            bio = row.get('bio')
            title = row.get('title')
            is_active = row.get('is_active') == 'True'

            try:
                user = User.objects.get(id=user_id)

                instructor = Instructor.objects.create(
                    user=user,
                    bio=bio,
                    title=title,
                    is_active=is_active
                )

                print(f'Instructor "{user.username}" created successfully.')
            except User.DoesNotExist:
                print(f'User with id {user_id} not found. Ignoring.')
            
        elif model == 'students':
            user_id = row.get('user_id')
            bio = row.get('bio')
            is_active = row.get('is_active') == 'True'

            try:
                user = User.objects.get(id=user_id)

                student = Student.objects.create(
                    user=user,
                    bio=bio,
                    is_active=is_active
                )

                print(f'Student "{user.username}" created successfully.')
            except User.DoesNotExist:
                print(f'User with id {user_id} not found. Ignoring.')
        elif model == 'progress':
            student_id = row.get('student_id')
            course_id = row.get('course_id')
            lesson_id = row.get('lesson_id')
            status = row.get('status')
            
            try:
                student = Student.objects.get(id=student_id)
                user = student.user
                course = Course.objects.get(id=course_id)
                lesson = Lesson.objects.get(id=lesson_id)
                
                progress = Progress.objects.create(
                    student=user,
                    course=course,
                    lesson=lesson,
                    status=status
                )

                print(f'Progress "{status}" created successfully.')
            except Student.DoesNotExist:
                print(f'Student with id {student_id} not found. Ignoring.')
            except Course.DoesNotExist:
                print(f'Course with id {course_id} not found. Ignoring.')
            except Lesson.DoesNotExist:
                print(f'Lesson with id {lesson_id} not found. Ignoring.')    
        elif model == 'lessons':
            course_id = row.get('course_id')
            title = row.get('title')
            content = row.get('content', '')
            order = row.get('order', '')
            duration_str = row.get('duration')
            video_url = row.get('video_url', '')

            print(title)

            try:
                course = Course.objects.get(id=course_id)
                
                lesson = Lesson.objects.create(
                    course=course,
                    title=title,
                    content=content,
                    order=int(order),
                    duration=parse_duration(duration_str),
                    video_url=video_url
                )

                print(f'Lesson "{title}" created successfully.')
            except Course.DoesNotExist:
                print(f'Course with id {course_id} not found. Ignoring.')
        elif model == 'courses':
            title = row.get('title')
            description = row.get('description')

            course = Course.objects.create(
                title=title,
                description=description
            )

            instructor_usernames = [name.strip() for name in row['instructors'].split(';') if name.strip()]
            for username in instructor_usernames:
                instructor = User.objects.filter(username=username, role='INSTRUCTOR').first()
                if instructor:
                    course.instructors.add(instructor)

            student_usernames = [name.strip() for name in row['students'].split(';') if name.strip()]
            for username in student_usernames:
                student = User.objects.filter(username=username, role='STUDENT').first()
                if student:
                    course.students.add(student)

            print(f'Course "{title}" created successfully.')

def parse_duration(value):
    """Converte uma string HH:MM:SS em timedelta"""
    if not value:
        return None
    try:
        h, m, s = map(int, value.split(':'))
        return timedelta(hours=h, minutes=m, seconds=s)
    except ValueError:
        print(f"Duração inválida: {value}")
        return None

read_csv_file(users_csv_path)
read_csv_file(instructors_csv_path)
read_csv_file(students_csv_path)
read_csv_file(courses_csv_path)
read_csv_file(lessons_csv_path)
read_csv_file(progress_csv_path)

print("Import completed")