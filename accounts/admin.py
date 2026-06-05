from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Department, Specialization, Level, StudentProfile, TeacherProfile


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