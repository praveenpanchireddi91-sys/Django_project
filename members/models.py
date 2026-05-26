from django.db import models


class Student(models.Model):

    name = models.CharField(max_length=100)

    pin = models.CharField(max_length=20)

    password = models.CharField(max_length=100)

    email = models.EmailField(unique=True)

    YEAR_CHOICES = [
        (1, 'First Year'),
        (2, 'Second Year'),
        (3, 'Third Year'),
    ]

    year = models.IntegerField(choices=YEAR_CHOICES, default=1)

    def __str__(self):
        return self.name


class Teacher(models.Model):

    name = models.CharField(max_length=100)

    password = models.CharField(max_length=100)

    email = models.EmailField(unique=True)

    def __str__(self):
        return self.name


class Attendance(models.Model):

    student = models.ForeignKey(Student, on_delete=models.CASCADE)

    date = models.DateField()

    status = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.student.name} - {self.date}"