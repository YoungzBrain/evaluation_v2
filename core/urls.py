from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('django-admin/', admin.site.urls),
    path('',              include('accounts.urls')),
    path('',              include('courses.urls')),      # Module 3 — matieres
    path('',              include('questions.urls')),    # Module 4 — questions
    path('',              include('evaluations.urls')),  # Module 5 — evaluations
]

# Servir les fichiers media en développement
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)