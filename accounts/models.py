from django.db import models
from django.contrib.auth.models import AbstractUser


class Department(models.Model):
    name        = models.CharField(max_length=150, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Specialization(models.Model):
    name        = models.CharField(max_length=150)
    department  = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name='specializations'
    )
    description = models.TextField(blank=True, null=True)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    class Meta:
        ordering        = ['name']
        unique_together = ('name', 'department')

    def __str__(self):
        return f"{self.name} ({self.department})"


class Level(models.Model):
    name  = models.CharField(max_length=50, unique=True)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name


class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin',   'Admin'),
        ('teacher', 'Teacher'),
        ('student', 'Student'),
    ]
    role      = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')
    is_active = models.BooleanField(default=True)

    def is_admin(self):
        return self.role == 'admin'

    def is_teacher(self):
        return self.role == 'teacher'

    def is_student(self):
        return self.role == 'student'

    def has_completed_profile(self):
        if self.role == 'student':
            return hasattr(self, 'student_profile')
        elif self.role == 'teacher':
            return hasattr(self, 'teacher_profile')
        return True  # admin always complete

    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.role})"


class StudentProfile(models.Model):
    user           = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='student_profile'
    )
    department     = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        null=True,
        related_name='students'
    )
    level          = models.ForeignKey(
        Level,
        on_delete=models.SET_NULL,
        null=True,
        related_name='students'
    )
    specialization = models.ForeignKey(
        Specialization,
        on_delete=models.SET_NULL,
        null=True,
        related_name='students'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Profile of {self.user}"


class TeacherProfile(models.Model):
    user        = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='teacher_profile'
    )
    departments = models.ManyToManyField(
        Department,
        related_name='teachers',
        blank=True
    )
    created_at  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Profile of {self.user}"


# --- Signals: auto-create TeacherProfile when a teacher user is created ---
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=User)
def ensure_teacher_profile(sender, instance, created, **kwargs):
    if created and instance.role == 'teacher':
        TeacherProfile.objects.get_or_create(user=instance)