import os
import django
from datetime import date

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here

from main_app.models import Student


def add_students():
    student = Student(
        student_id='FC5204',
        first_name='John',
        last_name='Doe',
        birth_date='1995-05-15',
        email='john.doe@university.com'
    )
    student.save()

    student = Student(
        student_id='FE0054',
        first_name='Jane',
        last_name='Smith',
        email='jane.smith@university.com'
    )
    student.save()

    student = Student(
        student_id='FH2014',
        first_name='Alice',
        last_name='Johnson',
        birth_date='1998-02-10',
        email='alice.johnson@university.com'
    )
    student.save()

    student = Student(
        student_id='FH2015',
        first_name='Bob',
        last_name='Wilson',
        birth_date='1996-11-25',
        email='bob.wilson@university.com'
    )
    student.save()


def get_students_info():
    all_students = Student.objects.all()
    result = ''
    for student in all_students:
        result += f'Student №{student.student_id}: {student.first_name} {student.last_name}; Email: {student.email}\n'
    return result


def update_students_emails():
    all_students = Student.objects.all()
    for student in all_students:
        new_email = student.email.replace("university.com", "uni-students.com")
        student.email = new_email
        student.save()


def truncate_students():
    all_students = Student.objects.all()
    all_students.delete()

# Run and print your queries

# 1. add_students()
# 1a. print(Student.objects.all())
# 2. print(get_students_info())
#3. update_students_emails()
#3a. for student in Student.objects.all():
#3b.     print(student.email)
# 4. truncate_students()
# 4a. print(Student.objects.all())
# 4b. print(f"Number of students: {Student.objects.count()}")
