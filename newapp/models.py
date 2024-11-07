from django.db import models

# Create your models here.
from django.contrib.auth.models import User


class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('Student', 'Student'),
        ('Instructor', 'Instructor'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    

class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(null=True,blank=True)
    content = models.TextField(null=True,blank=True)
    instructor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="courses")
    students = models.ManyToManyField(User, related_name="enrolled_courses", blank=True)