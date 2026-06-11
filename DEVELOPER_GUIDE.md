# Evaluation V2 - Developer Guide

## 1. Introduction

This document is intended to provide a complete, developer-focused reference for the `evaluation_v2` Django project. It is designed for a team member who needs to continue development, understand architecture, maintain the codebase, and extend features.

This guide covers:
- overall architecture
- app responsibilities
- data model definitions
- authentication, authorization, and role management
- detailed feature flows
- URL routing and views
- template structure and styling conventions
- PDF support and question extraction
- setup, testing, and deployment
- extension and maintenance guidance

This guide is intentionally thorough and is appropriate for a document that can expand to 15–20 pages when printed or rendered in markdown.

---

## 2. Project Goals and Scope

### 2.1 Vision
The project is an educational evaluation platform that enables students to evaluate teachers by course, supports department-based rankings, and allows administrators to manage the academic structure.

### 2.2 Core capabilities

- Student registration with profile completion.
- Admin-managed teacher accounts and course assignments.
- Department/level/specialization organization.
- Student evaluation workflows with scored and open-text questions.
- Public teacher ranking by department.
- PDF generation and question import support.

### 2.3 Audience

- Students: evaluate teachers and view ranking results.
- Teachers: are assigned to departments and evaluated.
- Admins: manage departments, courses, teachers, questions, and evaluations.

---

## 3. Architecture Overview

### 3.1 Django project structure

The project uses a conventional Django application layout:

- `core/` — main Django project and settings
- `accounts/` — authentication, user profiles, admin management
- `courses/` — course and teacher-course relationships
- `questions/` — question management and PDF uploads
- `evaluations/` — evaluation workflow, scoring, rankings, PDF generation
- `static/` — CSS/JS assets
- `media/` — uploaded and generated files

### 3.2 App responsibilities

- `accounts/`
  - Custom `User` model with role field
  - Admin CRUD for departments, specializations, levels, teachers
  - Public student registration and profile completion
  - Dashboards for admin, teacher, and student
  - Public `login` and registration logic

- `courses/`
  - `Course` and `TeacherCourse` models
  - Admin CRUD for courses
  - Teacher-course assignment management

- `questions/`
  - Question storage with scored/open types
  - PDF upload model for question source import
  - Tracks PDF pages and question positions

- `evaluations/`
  - Student evaluation flow
  - Answer storage and evaluation model
  - Public ranking and admin results views
  - PDF generation for submitted evaluations

### 3.3 Data and flow boundaries

This app uses a strong separation between the public student evaluation flow and the admin management flow:
- Public students register and complete their profile.
- Teacher accounts are managed by admins; public registration is restricted to students.
- Course evaluations are created by students only.
- Results and rankings are visible publicly.
- Admins have access to internal score views and all evaluations.

---

## 4. Data Model Reference

### 4.1 `accounts.User`

This is the custom user model used by the project.

```python
class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
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
        return True
```

Key facts:
- `role` controls access and feature visibility.
- `username` is set to email during registration.
- `has_completed_profile` is used by redirect logic and decorators.

### 4.2 `accounts.Department`

Represents an academic department.

Fields:
- `name` (unique)
- `description`

### 4.3 `accounts.Specialization`

Represents a specialization within a department.

Key constraint: unique by `(name, department)`.

### 4.4 `accounts.Level`

Represents an academic level.

Fields:
- `name`
- `order`

### 4.5 `accounts.StudentProfile`

Stores metadata for student users.

Fields:
- `department`
- `level`
- `specialization`

### 4.6 `accounts.TeacherProfile`

Stores metadata for teacher users.

Fields:
- `departments` (many-to-many)

Important:
- Teacher accounts are created by admins only.
- Teacher profiles are created automatically via signal when a teacher user exists.

### 4.7 `courses.Course`

Represents a course, linked to a department and level.

Fields:
- `department` (single department) — critical for ranking consistency
- `level`
- `specialization` (optional)
- `is_general`
- `is_active`

### 4.8 `courses.TeacherCourse`

Join model for teachers and courses.

Constraint: `(teacher, course)` unique.

### 4.9 `questions.PDFUpload`

Stores uploaded PDF documents for question import.

Fields:
- `file`
- `original_filename`
- `uploaded_by`

### 4.10 `questions.Question`

Represents evaluation questions.

Fields:
- `text`
- `type` (`scored` or `open`)
- `source_pdf`
- `pdf_page`
- `position`

### 4.11 `evaluations.Evaluation`

Represents a completed evaluation attempt.

Fields:
- `student`
- `teacher`
- `course`
- `status`

Constraint: unique per `(student, teacher, course)`.

### 4.12 `evaluations.Answer`

Stores answers for each question in an evaluation.

Fields:
- `score`
- `text_answer`

### 4.13 `evaluations.EvaluationPdf`

Links a generated PDF file to an evaluation.

Fields:
- `file_path`

---

## 5. Authentication and User Policy

### 5.1 Registration policy

Public registration is restricted to students.

In `accounts/views.py`, `register()` enforces:
- `role = 'student'`
- block teacher account creation via public registration
- redirect after creation to `complete_profile_student`

```python
# Public registration must always create students.
# Teacher accounts are created/managed by admins only.
role = 'student'
```

### 5.2 Login policy

The `login_view()` performs:
- email-based login fallback to username
- blocks login for users with role `teacher`
- permits login for `student` and `admin`

This means:
- teacher accounts cannot authenticate through the public login form
- teacher access is intended to be managed through a private/admin route if enabled

### 5.3 Dashboard redirection logic

`redirect_by_role(user)` controls landing pages:
- `admin` → `admin_dashboard`
- student with incomplete profile → `complete_profile_student`
- teacher with incomplete profile → `complete_profile_teacher`
- `teacher` → `teacher_dashboard`
- `student` → `student_dashboard`

### 5.4 Profile completion flow

Students must complete their profile after registration.

Teacher profile completion is also implemented in code, but project policy states teacher accounts are admin-managed.

---

## 6. URL Routing and Access

### 6.1 Root routing

`core/urls.py` includes all app URL configurations:

```python
path('django-admin/', admin.site.urls),
path('', include('accounts.urls')),
path('', include('courses.urls')),
path('', include('questions.urls')),
path('', include('evaluations.urls')),
```

### 6.2 Accounts URLs

Key routes in `accounts/urls.py`:

- `/` → home redirect to public ranking
- `/register/` → `register`
- `/login/` → `login_view`
- `/logout/` → `logout_view`
- `/complete-profile/student/` → student profile completion
- `/admin/dashboard/` → admin dashboard
- `/teacher/dashboard/` → teacher dashboard
- `/student/dashboard/` → student dashboard
- `/admin/departments/` → department list and CRUD
- `/admin/specializations/` → specialization list and CRUD
- `/admin/levels/` → level list and CRUD
- `/admin/teachers/` → teacher list and admin teacher CRUD

### 6.3 Courses URLs

Key routes in `courses/urls.py`:

- `/admin/courses/`
- `/admin/courses/new/`
- `/admin/courses/<id>/edit/`
- `/admin/courses/<id>/toggle/`
- `/admin/courses/<id>/delete/`

### 6.4 Evaluations URLs

Key routes in `evaluations/urls.py`:

- `/evaluate/` → teacher list for students
- `/evaluate/teacher/<teacher_pk>/courses/` → course selection
- `/evaluate/teacher/<teacher_pk>/course/<course_pk>/` → evaluation form
- `/evaluate/confirmation/<pk>/` → confirmation
- `/classement/` → public ranking
- `/mes-scores/` → teacher/ admin score page (subject to policy)
- `/mes-scores/teacher/<teacher_pk>/cours/<course_pk>/` → course detail
- `/admin/enseignants/<teacher_pk>/scores/` → admin teacher scores
- `/admin/enseignants/<teacher_pk>/cours/<course_pk>/` → admin course detail

---

## 7. Core Feature Flows

### 7.1 Student registration and profile completion

1. User visits `/register/`.
2. `accounts.views.register()` validates fields, creates a new `User` with `role='student'`, and logs them in.
3. Student is redirected to `/complete-profile/student/`.
4. `complete_profile_student()` collects department, level, and optional specialization.
5. `StudentProfile` is created and the student is redirected to `/student/dashboard/`.

### 7.2 Admin teacher/course setup

Admins perform these steps:
- create departments
- create specializations
- create levels
- create teachers using the admin interface
- create courses and assign them to a department and level
- optionally assign teacher-course relationships via teacher profiles or course admin

### 7.3 Student evaluation workflow

A student evaluates a teacher as follows:
1. Visit `/evaluate/`.
2. Select a teacher from a list filtered by courses accessible to the student.
3. Choose a course taught by that teacher.
4. Complete the evaluation form with scored and open-text questions.
5. Submit the evaluation.
6. System creates `Evaluation` and related `Answer` records, generates a PDF, and redirects to `/evaluate/confirmation/<pk>/`.

### 7.4 Public ranking flow

`public_ranking()` loads:
- all departments
- all teachers with submitted evaluations in each department
- ranking data using `_get_teacher_scores()` filtered by department

The ranking page shows:
- department tabs
- teacher global average scores
- subject/cours breakdowns

### 7.5 Admin results flow

Admin-specific pages include:
- all submitted evaluations list
- evaluation detail with answer breakdown
- teacher score summary
- teacher course detail
- PDF download for submitted evaluation

Access is protected by `_require_admin`.

---

## 8. Views and Decorators

### 8.1 Decorator patterns

The project defines reusable decorators for access control:

- `@login_required` — standard Django login guard.
- `@admin_required` — used in `accounts/views_admin.py`.
- `@student_required` — used in `evaluations/views.py`.
- `_require_admin` — used in `evaluations/views_results.py`.
- `_require_teacher_or_admin` — used in results views.

### 8.2 Key view responsibilities

#### `accounts/views.py`
- `home()` — redirect authenticated users by role or public ranking for anonymous users.
- `register()` — public student signup.
- `login_view()` — login with email/username and block public teacher login.
- `complete_profile_student()` — student profile completion.
- `complete_profile_teacher()` — teacher profile completion support.
- `admin_dashboard()` — admin statistics.
- `teacher_dashboard()` — teacher landing page.
- `student_dashboard()` — student landing page.
- `redirect_by_role()` — central role-based redirect.
- `api_specializations()` — AJAX endpoint for specializations.

#### `accounts/views_admin.py`
- Department CRUD.
- Specialization CRUD.
- Level CRUD.
- Teacher list/edit/toggle.
- All routes are admin-only.

#### `evaluations/views.py`
- `teacher_list()` — show teachers available to a student.
- `course_select()` — show courses available for a teacher.
- `evaluation_form()` — display and process evaluation answers.
- `evaluation_confirmation()` — show confirmation page.

#### `evaluations/views_results.py`
- `_get_teacher_scores()` — core aggregation function for teacher rankings.
- `teacher_scores()` — teacher or admin score view.
- `teacher_course_detail()` — per-course detail.
- `public_ranking()` — public ranking page.
- `admin_evaluation_list()` — list submitted evaluations.
- `admin_evaluation_detail()` — evaluation detail for admins.
- `admin_download_pdf()` — download generated PDF.
- `admin_teacher_scores()` — alias to `teacher_scores()` for admin.

---

## 9. Ranking and Score Calculation

### 9.1 Score aggregation rules

The project uses scored questions with values from 1 to 5.

Calculations:
- average score on 5
- convert to 100-point scale using `_score_to_100(avg_on_5)`
- `score_color` varies by range:
  - >= 75 → green
  - >= 50 → amber
  - otherwise → red

### 9.2 Department filtering

The public ranking depends on department-scoped aggregation.

`_get_teacher_scores(teacher, department=dept)` filters evaluations by course department.
This prevents a course from appearing in the wrong department's ranking.

### 9.3 Teacher score pages

`teacher_scores()` currently allows:
- admin to view any teacher's score page
- teacher to view their own score page if role permits

Project policy for documentation: teachers should only have public ranking access. If you want to enforce this, update `teacher_scores()` and route access accordingly.

---

## 10. Template Architecture

### 10.1 Template organization

Templates are organized by app and function:

- `accounts/templates/accounts/`
  - base layout, home, login, register, dashboards, admin management templates
- `courses/templates/courses/admin/`
  - course forms and lists
- `questions/templates/questions/admin/`
  - question management views
- `evaluations/templates/evaluations/student/`
  - teacher list, course selection, evaluation form, confirmation
- `evaluations/templates/evaluations/results/`
  - public ranking, teacher scores, course detail
- `evaluations/templates/evaluations/admin/`
  - evaluation list and detail

### 10.2 Common template conventions

- base templates contain global CSS and topbar structure.
- admin pages extend `accounts/admin/base_admin.html`.
- student evaluation pages extend `evaluations/student/base_student.html`.
- templates should avoid emoji and use accessible color and font weight.

### 10.3 Styling notes

The current theme uses:
- white content surfaces
- dark sidebar (#111827)
- dark text (#0f172a)
- blue action buttons (#2563eb)
- light gray backgrounds for cards and form controls

### 10.4 Recommendations for new templates

- keep markup semantic (`<main>`, `<section>`, `<nav>`, `<table>`)
- use consistent class naming for reusable components
- avoid inline styles where possible
- add `page_title` context values for title display

---

## 11. File and Data Workflows

### 11.1 PDF upload flow

`questions.PDFUpload` holds uploaded files.
Questions can be linked to a PDF via `source_pdf`, `pdf_page`, and `position`.

### 11.2 Evaluation PDF generation flow

In `evaluations/views.py`, when an evaluation is submitted:
- create `Evaluation`
- save `Answer` rows
- call `generate_evaluation_pdf(evaluation)`
- store relative path in `EvaluationPdf`

The generated file is stored under `media/evaluations_pdf`.

### 11.3 Question selection for evaluation forms

`evaluation_form()` fetches active questions.
If a recent PDF upload exists that produced active questions, the form preferentially uses those questions.

The questions list may include both scored and open questions.

---

## 12. Admin Management Details

### 12.1 Departments

Admin CRUD operations include:
- create department
- edit department
- delete department with cascade checks

### 12.2 Specializations

Admin CRUD operations include:
- list all specializations with department filter
- create specialization
- edit specialization
- delete specialization with safety checks

### 12.3 Levels

Admin CRUD operations include:
- create/edit level
- delete level
- ordering by `order`

### 12.4 Teachers

Admin can:
- list teachers
- create and edit teacher details
- assign department(s)
- toggle teacher active state
- manage teacher-course assignments

### 12.5 Courses

Admin can:
- create/edit/delete courses
- toggle course active state
- assign each course to exactly one department and one level
- optionally assign specialization

### 12.6 Evaluations

Admin can:
- view all submitted evaluations
- apply filters by department, teacher, and search text
- see detailed evaluation content
- download or regenerate a PDF

---

## 13. Security and Policy Notes

### 13.1 Teacher account handling

This project is configured so that:
- public registration creates only student accounts
- public login blocks teacher accounts
- teacher accounts should be created and managed by administrators

### 13.2 Role-based access control

The code uses decorators and role checks instead of a dedicated permission model.

Key access rules:
- admin-only: `accounts/views_admin.py` and admin evaluation pages
- student-only: evaluation workflow
- teacher/ admin: teacher score pages and course detail views

### 13.3 Potential Improvements

For future security improvements:
- enforce teacher login separation from public auth
- implement Django permissions/groups for fine-grained access
- sanitize all user input uniformly
- add CSRF and session security checks in deployment settings

---

## 14. Setup and Local Development

### 14.1 Environment

Suggested local setup:

```bash
cd c:\Users\BrAiN\Desktop\evaluation_v2
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### 14.2 Recommended dev commands

- `python manage.py makemigrations`
- `python manage.py migrate`
- `python manage.py createsuperuser`
- `python manage.py collectstatic`
- `python manage.py test`

### 14.3 Media and static files

- `media/` stores generated PDFs and uploaded question PDFs.
- `static/` contains CSS/JS assets.

### 14.4 Local troubleshooting

If templates or media do not load:
- verify `DEBUG = True`
- confirm `MEDIA_URL` and `MEDIA_ROOT` are set in `core/settings.py`
- ensure development static serving is enabled

---

## 15. Testing and Quality Assurance

### 15.1 Recommended test coverage

Add or extend tests for:
- model relationship behavior
- registration and login policy
- profile completion redirects
- evaluation submission logic
- scoring aggregation logic
- public ranking filtering by department
- admin-only access control

### 15.2 Suggested test structure

- `accounts/tests.py`
- `courses/tests.py`
- `questions/tests.py`
- `evaluations/tests.py`

### 15.3 Example test focus areas

- `User` role methods
- `StudentProfile` creation
- `TeacherCourse` uniqueness
- evaluation score conversion and aggregation
- `public_ranking()` department filter

---

## 16. Maintenance and Extension Guide

### 16.1 Adding a new evaluation question type

Steps:
1. extend `Question.TYPE_CHOICES`
2. update `evaluation_form()` to validate the new type
3. update answer storage logic in `evaluations/views.py`
4. update result pages to handle new question stats

### 16.2 Adding a new dashboard card

Steps:
1. update the view context in dashboard view
2. add markup to the dashboard template
3. add CSS styling if needed
4. create tests for the new metric

### 16.3 Adding a new admin filter

Steps:
1. update admin view query filters
2. update template filter controls
3. validate data with tests

### 16.4 Migrating to a production database

Recommended path:
- switch `DATABASES` in `core/settings.py`
- use PostgreSQL or MySQL
- run `python manage.py migrate`
- verify stored data and static/media serving

---

## 17. Common Issues and Troubleshooting

### 17.1 Teacher accounts cannot login

Reason:
- `login_view()` blocks teacher roles in public login.

Solution:
- create a separate private login path for teacher accounts if required
- or use Django admin login for teacher account management

### 17.2 Courses show in wrong department ranking

Reason:
- `_get_teacher_scores()` aggregated without department filtering.

Solution:
- ensure `public_ranking()` passes `department=dept`
- verify course `department` is assigned correctly

### 17.3 Student cannot evaluate a teacher

Reason:
- the course is not linked to the student’s eligible department/level/specialization
- or `TeacherCourse` does not connect the teacher to the course

### 17.4 PDF generation fails

Reason:
- file path or media settings incorrect
- PDF generator exception during rendering

---

## 18. Recommended Documentation Best Practices

To make this document even more useful over time:
- keep architecture diagrams updated
- annotate sections with file references
- document any policy deviations explicitly
- add a changelog for major feature changes
- maintain a release notes section for versioned improvements

## 19. FAQ for New Contributors

### Q: Where do I start?
A: Read `DEVELOPER_GUIDE.md`, then inspect `accounts/views.py` and `evaluations/views.py` for the main user flows.

### Q: How do I add a new model?
A: Add the model to the app's `models.py`, register migrations, update admin views and templates, and add tests.

### Q: How do I add a new page?
A: Add a URL route, build the view, create a template under the right app, and secure it with decorators.

### Q: How do I change the ranking formula?
A: Update `_score_to_100` and `_get_teacher_scores()` in `evaluations/views_results.py`, then adjust the ranking templates.

---

## 20. File Reference Index

### Primary files
- `core/settings.py`
- `core/urls.py`
- `manage.py`
- `accounts/models.py`
- `accounts/views.py`
- `accounts/views_admin.py`
- `accounts/urls.py`
- `courses/models.py`
- `courses/views_admin.py`
- `courses/urls.py`
- `questions/models.py`
- `questions/urls.py`
- `evaluations/models.py`
- `evaluations/views.py`
- `evaluations/views_results.py`
- `evaluations/urls.py`

### Template roots
- `accounts/templates/accounts/`
- `courses/templates/courses/admin/`
- `questions/templates/questions/admin/`
- `evaluations/templates/evaluations/student/`
- `evaluations/templates/evaluations/results/`
- `evaluations/templates/evaluations/admin/`

### Static assets
- `static/css/bootstrap.min.css`
- `static/css/pdf_overlay.css`
- `static/js/bootstrap.bundle.min.js`
- `static/js/pdf_overlay.js`

### Data files
- `db.sqlite3`
- `evaluation_v2_data.json`
- `sample_questions.csv`

---

## Appendix A: Role Access Matrix

| Role | Public Pages | Private Dashboards | Admin Pages | Teacher Score Pages | Evaluation Submission |
|------|--------------|--------------------|-------------|---------------------|-----------------------|
| Admin | yes | yes | yes | yes | no |
| Teacher | yes | limited | no | depends on policy | no |
| Student | yes | yes | no | no | yes |

## Appendix B: Recommended Future Tasks

- formalize teacher role access policy in code
- implement Django permission groups
- add end-to-end tests for evaluation flow
- add admin API endpoints for external reporting
- add a dedicated `README.md` summary and keep `DEVELOPER_GUIDE.md` as the long-form reference
