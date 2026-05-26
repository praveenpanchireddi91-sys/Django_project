from django.contrib import admin
from .models import Student, Teacher, Attendance


class StudentAdmin(admin.ModelAdmin):

    list_display = ("name", "pin", "email", "year")


admin.site.register(Student, StudentAdmin)


class TeacherAdmin(admin.ModelAdmin):

    list_display = ("name", "email")


admin.site.register(Teacher, TeacherAdmin)


class AttendanceAdmin(admin.ModelAdmin):

    list_display = ("student", "date", "status")


admin.site.register(Attendance, AttendanceAdmin)