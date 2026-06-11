from django.urls import path
from . import views_admin

urlpatterns = [
    # ── Liste ────────────────────────────────────────────────────────────────
    path('admin/questions/',                       views_admin.question_list,   name='question_list'),

    # ── CRUD ─────────────────────────────────────────────────────────────────
    path('admin/questions/new/',                   views_admin.question_create, name='question_create'),
    path('admin/questions/<int:pk>/edit/',          views_admin.question_edit,   name='question_edit'),
    path('admin/questions/<int:pk>/delete/',        views_admin.question_delete, name='question_delete'),

    # ── Toggle actif / inactif ────────────────────────────────────────────────
    path('admin/questions/<int:pk>/toggle/',        views_admin.question_toggle, name='question_toggle'),

    # ── Import CSV ────────────────────────────────────────────────────────────
    path('admin/questions/import/',                views_admin.question_import, name='question_import'),
    # PDF admin functions disabled - not yet implemented
    # path('admin/questions/pdfs/',                  views_admin.pdf_list, name='pdf_list'),
    # path('admin/questions/pdfs/<int:pk>/manage/',  views_admin.pdf_manage, name='pdf_manage'),
]