from django.contrib import admin
from .models import Course, TeacherCourse


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'department', 'level', 'specialization', 'is_general', 'is_active')
    list_filter = ('department', 'level', 'is_general', 'is_active')
    search_fields = ('name', 'department__name')


@admin.register(TeacherCourse)
class TeacherCourseAdmin(admin.ModelAdmin):
    list_display = ('teacher', 'course', 'created_at')
    list_filter = ('course__department', 'course__level')
    search_fields = ('teacher__username', 'teacher__first_name', 'teacher__last_name', 'course__name')
from django.contrib import admin

# Register your models here.
