from django.db import models
from django.conf import settings
from accounts.models import Department, Specialization, Level


class Course(models.Model):
    name           = models.CharField(max_length=150)
    description    = models.TextField(blank=True, null=True)
    department     = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name='courses'
    )
    level          = models.ForeignKey(
        Level,
        on_delete=models.CASCADE,
        related_name='courses'
    )
    specialization = models.ForeignKey(
        Specialization,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='courses'
    )
    is_general     = models.BooleanField(
        default=False,
        help_text="If True, all students in the same department and level can evaluate"
    )
    is_active      = models.BooleanField(default=True)
    created_at     = models.DateTimeField(auto_now_add=True)
    updated_at     = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['department', 'level', 'name']

    def __str__(self):
        return f"{self.name} ({self.department} — {self.level})"


class TeacherCourse(models.Model):
    teacher    = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='teacher_courses',
        limit_choices_to={'role': 'teacher'}
    )
    course     = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='teacher_courses'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('teacher', 'course')

    def __str__(self):
        return f"{self.teacher} — {self.course}"