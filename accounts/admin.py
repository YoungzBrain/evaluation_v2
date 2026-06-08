from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Department, Specialization, Level, StudentProfile, TeacherProfile
from courses.models import TeacherCourse


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display  = ('username', 'email', 'role', 'is_active', 'date_joined')
    list_filter   = ('role', 'is_active')
    search_fields = ('username', 'email')
    fieldsets     = UserAdmin.fieldsets + (
        ('Role', {'fields': ('role',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Role', {'fields': ('role',)}),
    )
    inlines = []


class TeacherProfileInline(admin.StackedInline):
    model = TeacherProfile
    can_delete = False
    verbose_name = 'Teacher profile'
    verbose_name_plural = 'Teacher profile'
    filter_horizontal = ('departments',)
    fk_name = 'user'



@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display  = ('name', 'description', 'created_at')
    search_fields = ('name',)


@admin.register(Specialization)
class SpecializationAdmin(admin.ModelAdmin):
    list_display  = ('name', 'department', 'created_at')
    list_filter   = ('department',)
    search_fields = ('name',)


@admin.register(Level)
class LevelAdmin(admin.ModelAdmin):
    list_display = ('name', 'order')
    ordering     = ('order',)


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'department', 'level', 'specialization')


@admin.register(TeacherProfile)
class TeacherProfileAdmin(admin.ModelAdmin):
    list_display = ('user',)
    filter_horizontal = ('departments',)
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'user__email')
    inlines = []


class TeacherCourseInline(admin.TabularInline):
    model = TeacherCourse
    fk_name = 'teacher'
    extra = 1
    verbose_name = 'Assigned course'
    verbose_name_plural = 'Assigned courses'

# Attach inline to TeacherProfileAdmin via UserAdmin is tricky; instead, register an inline
# on TeacherProfile by creating a simple proxy admin below.
# Attach the inlines to the User admin so admins can manage teacher profile and assigned courses
CustomUserAdmin.inlines = [TeacherProfileInline, TeacherCourseInline]