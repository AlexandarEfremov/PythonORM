# Generated by Django 5.0.4 on 2024-07-08 21:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0003_studentenrollment_alter_student_subjects'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentenrollment',
            name='grade',
            field=models.CharField(choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'), ('F', 'F')], max_length=1),
        ),
    ]