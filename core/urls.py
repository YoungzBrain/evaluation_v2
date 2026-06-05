from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('django-admin/', admin.site.urls),
    path('',              include('accounts.urls')),
    path('',              include('courses.urls')),   # Module 3 — matieres
    path('',              include('questions.urls')), # Module 4 — questions
]