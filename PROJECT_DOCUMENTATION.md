# Educational Evaluation Platform - Project Documentation

**Project Name:** Evaluation V2  
**Type:** Django Web Application  
**Purpose:** Comprehensive student evaluation system for teachers with department-based organization and public ranking system  
**Last Updated:** June 2026  

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Technology Stack](#technology-stack)
3. [Project Structure](#project-structure)
4. [Database Schema & Models](#database-schema--models)
5. [Authentication & Authorization](#authentication--authorization)
6. [Application Modules](#application-modules)
7. [URL Routing](#url-routing)
8. [Key Features](#key-features)
9. [UI/Theme System](#uitheme-system)
10. [Setup & Installation](#setup--installation)
11. [Development Notes](#development-notes)
12. [Known Issues & Fixes](#known-issues--fixes)

---

## Project Overview

The Educational Evaluation Platform is a Django-based system designed to:
- Allow students to evaluate teachers across different courses
- Organize evaluations by department, level, and specialization
- Display public teacher rankings by department
- Provide admin dashboard for system management
- Support PDF generation for evaluation records
- Extract questions from PDF documents

### Core Philosophy

- **Role-Based Access**: Admin, Teacher, and Student roles with specific permissions
- **Department-Centric**: All courses belong to exactly one department; teachers can work across multiple departments
- **Multi-Level Organization**: Students assigned to department, level, and specialization
- **Integrity**: Courses linked to single department to maintain accurate department-based rankings

---

## Technology Stack

- **Backend Framework**: Django 6.0.6
- **Database**: SQLite (default, configurable)
- **Python Version**: 3.x
- **Frontend**: HTML5, CSS3, Bootstrap
- **Template Engine**: Django Templates
- **Form Handling**: Django Forms
- **PDF Processing**: PDF generation and parsing capabilities
- **Static Files**: CSS (Bootstrap + custom), JavaScript
- **Authentication**: Django's built-in authentication with custom User model

---

## Project Structure

```
evaluation_v2/
├── core/                      # Django project settings
│   ├── settings.py           # Project configuration
│   ├── urls.py               # Root URL routing
│   ├── wsgi.py               # WSGI application
│   └── asgi.py               # ASGI application
│
├── accounts/                  # User authentication & profiles (Module 1)
│   ├── models.py             # User, TeacherProfile, StudentProfile, Department, Level, Specialization
│   ├── views.py              # Authentication views (login, register, dashboards)
│   ├── views_admin.py        # Admin management views (departments, levels, teachers, specializations)
│   ├── urls.py               # URL routing for accounts
│   ├── admin.py              # Django admin configuration
│   ├── apps.py               # App configuration
│   ├── management/
│   │   └── commands/
│   │       └── seed_levels.py # Management command to seed Level data
│   ├── migrations/           # Database migrations
│   └── templates/accounts/   # HTML templates
│       ├── base.html         # Base template with topbar & styling
│       ├── home.html         # Landing page
│       ├── login.html        # Login form
│       ├── register.html     # Registration form
│       ├── admin_dashboard.html
│       ├── student_dashboard.html
│       ├── teacher_dashboard.html
│       ├── complete_profile_student.html
│       └── admin/            # Admin management templates
│           ├── base_admin.html
│           ├── department_list.html
│           ├── level_list.html
│           ├── specialization_list.html
│           ├── teacher_list.html
│           ├── teacher_form.html
│           └── [various form/list templates]
│
├── courses/                   # Course management (Module 3)
│   ├── models.py             # Course, TeacherCourse models
│   ├── views_admin.py        # Course list, create, edit, delete, toggle
│   ├── urls.py               # Course URL routing
│   ├── admin.py              # Django admin configuration
│   ├── apps.py               # App configuration
│   ├── migrations/           # Database migrations
│   └── templates/courses/
│       └── admin/
│           ├── course_list.html
│           └── course_form.html
│
├── questions/                 # Question management (Module 4)
│   ├── models.py             # Question, PDFUpload models
│   ├── views.py              # Question views (if any)
│   ├── views_admin.py        # Question admin views
│   ├── urls.py               # Question URL routing
│   ├── admin.py              # Django admin configuration
│   ├── apps.py               # App configuration
│   ├── migrations/           # Database migrations
│   └── templates/questions/
│       └── admin/            # Question management templates
│
├── evaluations/               # Evaluation & results (Modules 5 & 6)
│   ├── models.py             # Evaluation, Answer, EvaluationPdf models
│   ├── views.py              # Student evaluation flow (teacher list, course select, form)
│   ├── views_results.py      # Results & ranking views (public ranking, teacher scores, details)
│   ├── pdf_generator.py      # PDF generation logic
│   ├── pdf_converter.py      # PDF processing utilities
│   ├── urls.py               # Evaluation URL routing
│   ├── admin.py              # Django admin configuration
│   ├── apps.py               # App configuration
│   ├── migrations/           # Database migrations
│   └── templates/evaluations/
│       ├── admin/            # Admin evaluation templates
│       │   ├── evaluation_list.html
│       │   └── evaluation_detail.html
│       ├── results/          # Public ranking & results templates
│       │   ├── public_ranking.html
│       │   ├── teacher_scores.html
│       │   └── course_detail.html
│       └── student/          # Student evaluation flow templates
│           ├── base_student.html
│           ├── teacher_list.html
│           ├── course_select.html
│           ├── evaluation_form.html
│           └── evaluation_confirmation.html
│
├── media/                     # User-uploaded files
│   ├── evaluations_pdf/      # Generated evaluation PDFs
│   └── questions_pdfs/       # Uploaded question PDFs
│
├── static/                    # Static files
│   ├── css/
│   │   ├── bootstrap.min.css # Bootstrap framework
│   │   └── pdf_overlay.css   # Custom styling
│   └── js/
│       ├── bootstrap.bundle.min.js
│       └── pdf_overlay.js
│
├── manage.py                  # Django management script
├── db.sqlite3                 # SQLite database
├── requirements.txt           # Python dependencies
└── venv/                      # Python virtual environment
```

---

## Database Schema & Models

### 1. **accounts.Department**
Organizational unit for courses and teachers.

| Field | Type | Details |
|-------|------|---------|
| id | AutoField | Primary key |
| name | CharField(150) | Unique department name |
| description | TextField | Optional description |
| created_at | DateTimeField | Auto-set on creation |
| updated_at | DateTimeField | Auto-updated |

### 2. **accounts.Specialization**
Specialization within a department (e.g., "Web Development" under IT department).

| Field | Type | Details |
|-------|------|---------|
| id | AutoField | Primary key |
| name | CharField(150) | Name of specialization |
| department | ForeignKey | References Department (CASCADE) |
| description | TextField | Optional description |
| created_at | DateTimeField | Auto-set on creation |
| updated_at | DateTimeField | Auto-updated |
| **Constraint** | unique_together | (name, department) |

### 3. **accounts.Level**
Academic level (e.g., Year 1, Year 2, Year 3).

| Field | Type | Details |
|-------|------|---------|
| id | AutoField | Primary key |
| name | CharField(50) | Unique level name |
| order | PositiveSmallIntegerField | Ordering (ascending) |

### 4. **accounts.User** (Custom AbstractUser)
Extended Django User model with role-based access.

| Field | Type | Details |
|-------|------|---------|
| id | AutoField | Primary key |
| username | CharField | From AbstractUser |
| password | CharField | From AbstractUser |
| email | EmailField | From AbstractUser |
| first_name | CharField | From AbstractUser |
| last_name | CharField | From AbstractUser |
| role | CharField(10) | Choices: 'admin', 'teacher', 'student' (default: 'student') |
| is_active | BooleanField | Account active/inactive |
| **Methods** | | `is_admin()`, `is_teacher()`, `is_student()`, `has_completed_profile()` |

### 5. **accounts.StudentProfile**
Profile extension for student users.

| Field | Type | Details |
|-------|------|---------|
| id | AutoField | Primary key |
| user | OneToOneField | References User (CASCADE, related_name='student_profile') |
| department | ForeignKey | References Department (SET_NULL, nullable) |
| level | ForeignKey | References Level (SET_NULL, nullable) |
| specialization | ForeignKey | References Specialization (SET_NULL, nullable) |
| created_at | DateTimeField | Auto-set on creation |

### 6. **accounts.TeacherProfile**
Profile extension for teacher users.

| Field | Type | Details |
|-------|------|---------|
| id | AutoField | Primary key |
| user | OneToOneField | References User (CASCADE, related_name='teacher_profile') |
| departments | ManyToManyField | References Department (multiple departments allowed) |
| created_at | DateTimeField | Auto-set on creation |
| **Signal** | post_save | Auto-creates TeacherProfile when teacher user is created |

### 7. **courses.Course**
Course offered to students for evaluation.

| Field | Type | Details |
|-------|------|---------|
| id | AutoField | Primary key |
| name | CharField(150) | Course name |
| description | TextField | Optional description |
| department | ForeignKey | References Department (CASCADE, **CRITICAL**: one department per course) |
| level | ForeignKey | References Level (CASCADE) |
| specialization | ForeignKey | References Specialization (SET_NULL, nullable, optional) |
| is_general | BooleanField | If True, all students in department/level can evaluate |
| is_active | BooleanField | Course active/inactive |
| created_at | DateTimeField | Auto-set on creation |
| updated_at | DateTimeField | Auto-updated |

### 8. **courses.TeacherCourse**
Junction table linking teachers to courses.

| Field | Type | Details |
|-------|------|---------|
| id | AutoField | Primary key |
| teacher | ForeignKey | References User with role='teacher' (CASCADE) |
| course | ForeignKey | References Course (CASCADE) |
| created_at | DateTimeField | Auto-set on creation |
| **Constraint** | unique_together | (teacher, course) |

### 9. **questions.PDFUpload**
PDF document uploaded for question extraction.

| Field | Type | Details |
|-------|------|---------|
| id | AutoField | Primary key |
| file | FileField | upload_to='questions_pdfs/' |
| original_filename | CharField(255) | Original filename |
| uploaded_by | ForeignKey | References User (SET_NULL, nullable) |
| created_at | DateTimeField | Auto-set on creation |

### 10. **questions.Question**
Evaluation question (scored or open text).

| Field | Type | Details |
|-------|------|---------|
| id | AutoField | Primary key |
| text | TextField | Question text |
| type | CharField(10) | Choices: 'scored' (1-5), 'open' (text) |
| is_active | BooleanField | Question active/inactive |
| source_pdf | ForeignKey | References PDFUpload (SET_NULL, nullable) |
| pdf_page | PositiveIntegerField | Page number in PDF (nullable) |
| position | PositiveIntegerField | Order within PDF (nullable) |
| created_at | DateTimeField | Auto-set on creation |
| updated_at | DateTimeField | Auto-updated |

### 11. **evaluations.Evaluation**
Student evaluation of a teacher for a course.

| Field | Type | Details |
|-------|------|---------|
| id | AutoField | Primary key |
| student | ForeignKey | References User with role='student' (CASCADE) |
| teacher | ForeignKey | References User with role='teacher' (CASCADE) |
| course | ForeignKey | References Course (CASCADE) |
| status | CharField(10) | Choices: 'pending', 'submitted' (default: 'pending') |
| created_at | DateTimeField | Auto-set on creation |
| updated_at | DateTimeField | Auto-updated |
| **Constraint** | unique_together | (student, teacher, course) |

### 12. **evaluations.Answer**
Individual answer to a question within an evaluation.

| Field | Type | Details |
|-------|------|---------|
| id | AutoField | Primary key |
| evaluation | ForeignKey | References Evaluation (CASCADE) |
| question | ForeignKey | References Question (CASCADE) |
| score | PositiveSmallIntegerField | 1-5 for scored questions (nullable) |
| text_answer | TextField | Response for open questions (nullable) |
| created_at | DateTimeField | Auto-set on creation |
| **Constraint** | unique_together | (evaluation, question) |

### 13. **evaluations.EvaluationPdf**
Generated PDF for completed evaluation.

| Field | Type | Details |
|-------|------|---------|
| id | AutoField | Primary key |
| evaluation | OneToOneField | References Evaluation (CASCADE) |
| file_path | CharField(255) | Path to generated PDF |
| generated_at | DateTimeField | Auto-set on creation |

### Entity Relationship Diagram

```
┌─────────────────┐
│ User (Custom)   │
├─────────────────┤
│ id (PK)         │
│ username        │
│ email           │
│ role            │
│ is_active       │
└────────┬────────┘
         │
    ┌────┴──────────────────┐
    │                       │
    ▼                       ▼
┌──────────────────┐  ┌──────────────────┐
│ StudentProfile   │  │ TeacherProfile   │
├──────────────────┤  ├──────────────────┤
│ user (1:1) ◄────┼──┤ user (1:1) ◄─────┤
│ department (FK)  │  │ departments (M:M)│
│ level (FK)       │  └──────────────────┘
│ specialization   │         │
│ (FK)             │         │
└──────────────────┘         │
         │                   │
         └───────────────┐   │
                         │   │
                  ┌──────▼──▼────────┐
                  │ Department       │
                  ├──────────────────┤
                  │ id (PK)          │
                  │ name             │
                  │ description      │
                  └──────────────────┘
                         │
        ┌────────────────┼───────────────┐
        │                │               │
        ▼                ▼               ▼
    ┌────────┐  ┌──────────────────┐  ┌─────────────┐
    │ Course │  │Specialization    │  │ Level       │
    ├────────┤  ├──────────────────┤  ├─────────────┤
    │id (PK) │  │id (PK)           │  │id (PK)      │
    │name    │  │name              │  │name         │
    │dept(FK)│  │dept (FK)         │  │order        │
    │level   │  └──────────────────┘  └─────────────┘
    │spec(FK)│
    │is_gen. │
    └────────┘
         │
    ┌────┴────────────────┐
    │                     │
    ▼                     ▼
┌────────────┐  ┌──────────────────┐
│TeacherCourse  Evaluation
├────────────┤  ├──────────────────┤
│teacher (FK)│  │student (FK)      │
│course (FK) │  │teacher (FK)      │
└────────────┘  │course (FK)       │
                │status            │
                └────────┬──────────┘
                         │
                         ▼
                    ┌─────────┐
                    │ Answer  │
                    ├─────────┤
                    │eval (FK)│
                    │quest(FK)│
                    │score    │
                    │text_ans │
                    └─────────┘
```

---

## Authentication & Authorization

### User Roles

1. **Admin** (`role='admin'`)
   - Full system access
   - Manage departments, specializations, levels, teachers, courses
   - View all evaluations and results
   - Access admin dashboard

2. **Teacher** (`role='teacher'`)
   - Assigned to department(s) by an admin
   - Can be evaluated by students
   - Can only view public rankings
   - Does not have access to private personal score or course detail pages
   - Teacher dashboard is limited to public ranking access

3. **Student** (`role='student'`)
   - Must complete profile with department, level, specialization
   - Can evaluate assigned teachers
   - View public rankings
   - Submit evaluations
   - Access student dashboard

### Role Access Matrix

| Role | Dashboard | Public Rankings | Evaluation Form | Course Management | Teacher Management |
|------|-----------|-----------------|----------------|-------------------|--------------------|
| Admin | Yes | Yes | No | Yes | Yes |
| Teacher | Yes (public rankings only) | Yes | No | No | No |
| Student | Yes | Yes | Yes | No | No |

### Decorators & Permission Checks

**In `accounts/views.py`:**
```python
@_require_admin          # Restricts to admin role
@_require_teacher_or_admin  # Restricts to teacher or admin
@login_required         # Django's standard login requirement
```

### Profile Completion Flow

1. **Student** registers → redirected to complete profile (select department, level, specialization)
2. **Admin** no profile completion required (managed separately via admin interface)

---

## Application Modules

### Module 1: Accounts (Authentication & Profiles)

**Purpose:** User management, authentication, role-based dashboards

**Key Views:**
- `student_dashboard` - Student overview
- `teacher_dashboard` - Teacher overview with public ranking access only

**Admin Management Views (views_admin.py):**
- Department: list, create, edit, delete
- Specialization: list, create, edit, delete
- Level: list, create, edit, delete
- Teacher: list, create, edit, toggle (activate/deactivate)

**Models:**
- User (custom AbstractUser)
- StudentProfile
- TeacherProfile
- Department
- Specialization
- Level

**URLs:** `/admin/[departments|specializations|levels|teachers]/...`

---

### Module 2: Accounts - Admin Dashboard

**Purpose:** Central management interface for system administrators

**Key Features:**
- Sidebar navigation with category grouping
- Dark sidebar (#111827), white main content area
- Responsive grid layout
- Comprehensive CRUD operations

**Templates:**
- `admin/base_admin.html` - Admin layout wrapper
- `admin/department_list.html` - Department list
- `admin/specialization_list.html` - Specialization list
- `admin/level_list.html` - Level list
- `admin/teacher_list.html` - Teacher list
- `admin/[resource]_form.html` - Form templates

---

### Module 3: Courses (Course Management)

**Purpose:** Define and manage courses offered by departments

**Key Views:**
- `course_list` - List all courses
- `course_create` - Create new course
- `course_edit` - Edit existing course
- `course_toggle` - Activate/deactivate course
- `course_delete` - Delete course

**Models:**
- Course
- TeacherCourse (linking teachers to courses)

**Critical Design:**
- **Each course belongs to exactly ONE department** - ensures accurate department-based rankings
- Courses linked to Level and optional Specialization
- `is_general` flag: if True, all students in department/level can evaluate

---

### Module 4: Questions (Question Management)

**Purpose:** Manage evaluation questions and import questions from PDF documents.

**Key Views & Features:**
- Question administration and activation
- PDF upload and question source tracking
- PDF page/position metadata for evaluation overlay

**Models:**
- `PDFUpload` stores uploaded PDFs for parsing and question sourcing
- `Question` stores scored and open questions, with optional PDF origin metadata

**Design Notes:**
- Question imports are used to overlay evaluation forms on PDF-based questionnaires.
- Active questions are used in evaluation forms; inactive questions are hidden.

---

### Module 5: Evaluations (Student Workflow)

**Purpose:** Student evaluation flow for selecting a teacher, selecting a course, submitting answers, and receiving confirmation.

**Key Views:**
- `teacher_list` - shows available teachers filtered by student profile
- `course_select` - shows courses taught by the selected teacher
- `evaluation_form` - displays and validates evaluation questions
- `evaluation_confirmation` - confirms successful submission

**Important logic:**
- Student can only evaluate teachers who are linked to courses accessible by their department, level, and specialization.
- Duplicate evaluations are prevented by a unique constraint on `(student, teacher, course)`.
- The evaluation form validates scored questions as integers 1–5.
- Submitted evaluations create `Evaluation` and related `Answer` records.
- A PDF of the completed evaluation is generated and stored in `media/evaluations_pdf/`.

---

### Module 6: Results & Rankings

**Purpose:** Aggregate evaluation results, display public rankings, and allow admin review of evaluations.

**Key Views:**
- `public_ranking` - department-based public teacher ranking
- `teacher_scores` - teacher score detail page
- `teacher_course_detail` - per-course breakdown
- `admin_evaluation_list` - list of submitted evaluations for admins
- `admin_evaluation_detail` - evaluation review page
- `admin_download_pdf` - download generated evaluation PDF

**Ranking design:**
- Teacher scores are aggregated by department using submitted evaluations.
- Each course score is converted from a 1-5 average to a 0-100 scale.
- Department filtering is applied to avoid cross-department leakage.

**Note:** Public ranking is the public home entry point for anonymous users.

---

## Views and Decorators

### Access control patterns

The codebase uses a combination of login decorators and explicit role checks:
- `@login_required` from Django
- `@admin_required` in `accounts/views_admin.py`
- `@student_required` in `evaluations/views.py`
- `_require_admin` and `_require_teacher_or_admin` in `evaluations/views_results.py`

### Role-aware redirects

`redirect_by_role(user)` centralizes landing page routing:
- `admin` → `admin_dashboard`
- `teacher` with incomplete profile → `complete_profile_teacher`
- `student` with incomplete profile → `complete_profile_student`
- `teacher` → `teacher_dashboard`
- `student` → `student_dashboard`

---

## Ranking and Score Calculation

### Score conversion rules

- Average score on 1–5 is converted to a percentage using:
  - `score_100 = round(avg_on_5 * 20, 1)`
- Score colors are assigned as:
  - `>= 75` → `green`
  - `>= 50` → `amber`
  - otherwise → `red`

### Department-scoped aggregation

`_get_teacher_scores(teacher, department)` filters evaluations by `course__department`.
This ensures a teacher is ranked only in departments where they actually have submitted evaluations.

### Public ranking logic

`public_ranking()` builds ranking data by:
- listing departments
- selecting teachers with submitted evaluations in each department
- calculating each teacher's department-specific average score
- rendering subject breakdowns for each teacher

---

## Templates and Theme

### Template organization

- `accounts/templates/accounts/` – auth, dashboards, admin UI
- `courses/templates/courses/admin/` – course admin pages
- `questions/templates/questions/admin/` – question admin pages
- `evaluations/templates/evaluations/student/` – student flows
- `evaluations/templates/evaluations/results/` – public ranking and teacher results
- `evaluations/templates/evaluations/admin/` – admin evaluation pages

### Theming conventions

- Light content surfaces with a dark sidebar
- Minimal emoji usage
- Consistent `page_title` context variable usage
- Responsive layout using Bootstrap classes

### Styling notes

- `static/css/bootstrap.min.css` for framework styles
- `static/css/pdf_overlay.css` for evaluation PDF overlays
- `static/js/pdf_overlay.js` for interactive PDF question positioning

---

## File and Data Workflows

### Evaluation PDF generation

When an evaluation is submitted, the system:
1. creates the `Evaluation` record
2. saves all `Answer` records
3. calls `generate_evaluation_pdf(evaluation)`
4. stores the returned relative path in `EvaluationPdf`

### Question PDF source selection

The evaluation form prefers questions from the most recent active `PDFUpload` if available.
This supports hybrid workflows where PDF-sourced questions are used instead of the default question set.

---

## Admin Management Details

### Department administration

Admin views allow full CRUD with validation and foreign key safety checks.

### Specializations

Admins can create specializations filtered by department and delete only when safe.

### Levels

Admins manage ordered levels.

### Teachers and courses

Admins can create or toggle teacher accounts and assign them to multiple departments.
Courses are created per department/level and linked to teachers via `TeacherCourse`.

### Evaluations

Admin evaluation pages include:
- list and filters for submitted evaluations
- search by teacher, student, or course name
- evaluation detail with both scored and open-text answers
- PDF download and regeneration support

---

## Security and Policy Notes

### Teacher account policy

Public registration is restricted to students only.
Teacher accounts are intended to be created and managed by admins.
Public login blocks users where `role == 'teacher'`.

### Role-based access summary

The platform enforces role access through decorators and explicit checks rather than a permissions framework.
This is a key area for future hardening if the project scales.

---

## Setup and Local Development

### Basic setup steps

```powershell
cd c:\Users\BrAiN\Desktop\evaluation_v2
python -m venv venv
venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

### Recommended commands

- `python manage.py makemigrations`
- `python manage.py migrate`
- `python manage.py test`
- `python manage.py collectstatic`

### Media and static files

- `media/` stores generated PDFs and uploaded question PDFs
- `static/` contains CSS and JavaScript assets

---

## Testing and Quality Assurance

### Suggested coverage areas

- authentication and role restrictions
- student registration and profile completion
- evaluation submission and duplicate prevention
- ranking aggregation by department
- public ranking output
- admin-only views and PDF download

### Suggested test files

- `accounts/tests.py`
- `courses/tests.py`
- `questions/tests.py`
- `evaluations/tests.py`

---

## Maintenance and Extension Guide

### Adding a new evaluation type

1. extend `Question.TYPE_CHOICES`
2. update `evaluation_form()` validation
3. update answer creation logic
4. update result page rendering

### Adding an admin filter

1. update query filters in the relevant admin view
2. update the template filter controls
3. add or update tests

### Preparing for production

- switch `DATABASES` to PostgreSQL or another production database
- configure `MEDIA_ROOT` and `STATIC_ROOT`
- secure `SECRET_KEY` and debug settings

---

## Common Issues and Troubleshooting

### Teacher login blocked unexpectedly

Reason: the public login code blocks `role == 'teacher'`.

### Rankings appear in multiple departments

Reason: course aggregation must filter by `course__department`.

### Student cannot evaluate a course

Reason: course is not accessible for the student's department/level/specialization, or the teacher-course link is missing.

---

## Recommended Documentation Best Practices

- keep architecture diagrams updated
- note any policy exceptions clearly
- maintain a changelog for major features
- use this document as the single source of truth for developer onboarding

---

## FAQ for New Contributors

**Where should I start?**
Read the Project Overview, then inspect `accounts/views.py` and `evaluations/views.py` for the main user flows.

**How do I add a new page?**
Add a URL route, a view, a template, and secure the view with the appropriate decorator.

**How do I change the ranking formula?**
Update `_score_to_100()` and `_get_teacher_scores()` in `evaluations/views_results.py`.

---

## File Reference Index

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

---

## Appendix A: Role Access Matrix

| Role | Public Pages | Private Dashboards | Admin Pages | Teacher Score Pages | Evaluation Submission |
|------|--------------|--------------------|-------------|---------------------|-----------------------|
| Admin | yes | yes | yes | yes | no |
| Teacher | yes | yes (restricted) | no | depends on policy | no |
| Student | yes | yes | no | no | yes |

---

## Appendix B: Recommended Future Tasks

- Formalize teacher access policy in code
- Implement Django groups and permissions
- Add end-to-end evaluation flow tests
- Add admin API endpoints for reporting
- Maintain a shorter `README.md` for project summary and keep this file as full documentation


**URLs:** `/admin/courses/...`

---

### Module 4: Questions (Question Management)

**Purpose:** Manage evaluation questions with PDF support

**Models:**
- Question (scored 1-5 or open text)
- PDFUpload (for extracting questions from PDFs)

**Key Features:**
- Questions can be sourced from PDF documents
- Tracks PDF page number and position
- Active/inactive toggle
- Support for two question types: scored and open-text

**URLs:** `/admin/questions/...`

---

### Module 5: Student Evaluation Flow

**Purpose:** Guide students through evaluating teachers

**Key Views:**
- `teacher_list` - Display teachers available for evaluation
- `course_select` - Select course for teacher evaluation
- `evaluation_form` - Complete evaluation (answer questions)
- `evaluation_confirmation` - Confirmation page after submission

**Flow:**
1. Student selects teacher from list
2. Selects course being evaluated
3. Answers all evaluation questions
4. Submits evaluation (status changes to 'submitted')
5. Receives confirmation

**Models:**
- Evaluation (links student → teacher → course)
- Answer (individual responses)

**URLs:** `/evaluate/...`

---

### Module 6: Results & Rankings

**Purpose:** Display evaluation results and teacher rankings

**Key Views (views_results.py):**
- `public_ranking` - Public teacher rankings by department
  - **FIXED:** Now filters courses by department to prevent cross-department display
  - Aggregates scores across evaluations using Django ORM (Avg, Count)
  - Converts 5-point scale to 100-point scale

- `teacher_scores` - Admin/hidden teacher score details (not available to teacher accounts in public mode)

- `teacher_course_detail` - Detailed breakdown for specific teacher/course (admin-only)
  - Individual question scores
  - Comments from evaluations

- `admin_teacher_scores` - Admin view of teacher scores

- `admin_course_detail` - Admin view of course details

**Score Calculation:**
- Questions scored 1-5
- Average calculated across all evaluations
- Converted to 100-point scale: `(avg_score - 1) * 25`
- Example: avg 4.5 = (4.5 - 1) * 25 = 87.5 points

**Bug Fix Applied:**
- **Issue:** Courses appeared in rankings for ALL teacher's departments
- **Root Cause:** `_get_teacher_scores()` fetched all teacher's courses without department filtering
- **Solution:** Added optional `department` parameter with query filter: `if department: query = query.filter(course__department=department)`
- **Backward Compatibility:** Parameter is optional; if not provided, all courses returned

**Templates:**
- `results/public_ranking.html` - Department-based rankings
- `results/teacher_scores.html` - Admin/hidden teacher score page
- `results/course_detail.html` - Detailed course breakdown

**URLs:** `/classement/`, `/mes-scores/` (admin/hidden), `/admin/...`

---

## URL Routing

### Root URL Configuration (`core/urls.py`)
```python
path('django-admin/', admin.site.urls)  # Django built-in admin
path('', include('accounts.urls'))      # App 1: Authentication
path('', include('courses.urls'))       # App 3: Courses
path('', include('questions.urls'))     # App 4: Questions
path('', include('evaluations.urls'))   # App 5 & 6: Evaluations & Results
```

### Complete URL Structure

#### Accounts (`accounts/urls.py`)
```
/                                   # home
/register/                          # register
/login/                             # login_view
/logout/                            # logout_view
/api/specializations/               # api_specializations (AJAX)
/complete-profile/student/          # complete_profile_student
/admin/dashboard/                   # admin_dashboard
/teacher/dashboard/                 # teacher_dashboard
/student/dashboard/                 # student_dashboard
/admin/departments/                 # department_list (C, R, U, D)
/admin/specializations/             # specialization_list (C, R, U, D)
/admin/levels/                      # level_list (C, R, U, D)
/admin/teachers/                    # teacher_list (C, R, U, D, toggle)
```

#### Courses (`courses/urls.py`)
```
/admin/courses/                     # course_list
/admin/courses/new/                 # course_create
/admin/courses/<id>/edit/           # course_edit
/admin/courses/<id>/toggle/         # course_toggle
/admin/courses/<id>/delete/         # course_delete
```

#### Questions (`questions/urls.py`)
```
/admin/questions/                   # question_list
/admin/questions/new/               # question_create
/admin/questions/<id>/edit/         # question_edit
/admin/questions/<id>/delete/       # question_delete
```

#### Evaluations (`evaluations/urls.py`)
```
/evaluate/                          # evaluation_teacher_list
/evaluate/teacher/<id>/courses/     # evaluation_course_select
/evaluate/teacher/<id>/course/<id>/ # evaluation_form
/evaluate/confirmation/<id>/        # evaluation_confirmation
/classement/                        # public_ranking
/mes-scores/                        # teacher_scores
/mes-scores/teacher/<id>/cours/<id>/ # teacher_course_detail
/admin/enseignants/<id>/scores/     # admin_teacher_scores
/admin/enseignants/<id>/cours/<id>/ # admin_course_detail
```

---

## Key Features

### 1. **Role-Based Access Control**
- Three distinct user roles with specific permissions
- Decorators for view protection
- Profile completion enforced before dashboard access

### 2. **Department-Based Organization**
- Courses strictly assigned to single department
- Teachers can work across multiple departments
- Rankings generated per department (with filtering)

### 3. **Multi-Level Hierarchy**
- Department → Specialization → Level → Course
- Students assigned to specific department, level, and specialization
- Supports general courses (department/level wide) or specialized

### 4. **Evaluation Workflow**
- Students evaluate teachers on specific courses
- Questions can be scored (1-5) or open-text
- Unique constraint: (student, teacher, course) prevents duplicate evaluations

### 5. **Results & Rankings**
- Public teacher rankings viewable by all
- Department-filtered rankings (courses only appear for their assigned department)
- Aggregated scores: average across evaluations, 5-point to 100-point conversion
- Detailed per-course breakdowns

### 6. **PDF Support**
- Upload evaluation forms as PDFs
- Extract questions from PDFs
- Generate PDF records of submitted evaluations
- Track PDF page numbers and question positioning

### 7. **Admin Dashboard**
- Centralized management interface
- CRUD operations for all entities
- Teacher activation/deactivation toggle
- Course activation/deactivation toggle
- Light theme UI with dark sidebar navigation

### 8. **API Endpoints**
- `/api/specializations/` - AJAX endpoint for fetching specializations by department

---

## UI/Theme System

### Light Theme (Current Implementation)

**Design Rationale:**
- Clean, professional appearance
- Improved contrast for readability
- Dark sidebar for navigation, white content areas for focus
- Consistent typography and spacing

**Color Palette:**

| Element | Color | Hex Code | Usage |
|---------|-------|----------|-------|
| Sidebar Background | Dark Gray | #111827 | Navigation area background |
| Main Content | White | #ffffff | Page content background |
| Text (Primary) | Dark Navy | #0f172a | Main text, headers |
| Text (Secondary) | Gray | #475569 | Secondary text, descriptions |
| Borders | Light Blue | #dbeafe, #e6eef8 | Card borders, separators |
| Button Primary | Blue | #2563eb | Primary action buttons |
| Button Hover | Dark Blue | #1d4ed8 | Button hover state |
| Steps Bar | Light Gray | #e5e7eb | Inactive step circles |
| Steps Highlight | Amber | #fbbf24 | Completed/selected steps |
| Badge (General) | Light Blue | Custom | General question badges |
| Badge (Specialized) | Light Purple | Custom | Specialized question badges |

**Typography:**
- Font Weight: 500-700 for improved readability on light backgrounds
- Minimum 500 for body text, 600-700 for emphasis
- Bootstrap font stack

**Component Styling:**

1. **Cards (.card-dark)**
   - White background, light borders
   - Subtle shadow for depth
   - Rounded corners (12px)

2. **Buttons (.btn-primary-custom, .btn-logout)**
   - Consistent sizing and spacing
   - Clear hover states
   - Accessible contrast ratios

3. **Forms**
   - White backgrounds for inputs
   - Dark text for visibility
   - Blue focus states
   - Light borders (default), darker on focus

4. **Tables (.table-dark-custom)**
   - White background cells
   - Dark text
   - Light borders
   - Readable header styling

5. **Progress/Steps**
   - Light gray inactive circles
   - Amber highlight for active/completed
   - Dark text labels

**Layout:**

1. **Topbar (.topbar)**
   - White background
   - Shadow for separation
   - Contains navigation and user menu

2. **Admin Sidebar (.admin-sidebar)**
   - Dark (#111827) background
   - 250px fixed width
   - Rounded corners, subtle border
   - Shadow for elevation

3. **Admin Layout (.admin-layout)**
   - Flexbox with gap spacing
   - Flush with viewport top (no top padding)
   - Padding on sides and bottom

4. **Main Container (.main)**
   - Padding: 0 2rem 2rem 2rem (no top padding)
   - Responsive width
   - Centered content

**Template Files Affected:**
- `accounts/templates/accounts/base.html` - Base styling, topbar, form elements
- `accounts/templates/accounts/admin/base_admin.html` - Admin layout
- `accounts/templates/accounts/student_dashboard.html` - Student page
- `evaluations/templates/evaluations/student/base_student.html` - Evaluation flow
- All admin list/form templates in respective app template folders

### Styling Framework

**Bootstrap Integration:**
- Bootstrap 5 for responsive grid and components
- Custom CSS overrides for theme consistency
- No emoji (removed in cleanup)

**Custom CSS:**
Located in `static/css/`:
- `bootstrap.min.css` - Bootstrap framework
- `pdf_overlay.css` - PDF-specific styling

---

## Setup & Installation

### Prerequisites
- Python 3.8+
- pip (Python package manager)
- Virtual environment tool (venv)

### Installation Steps

1. **Clone/Extract Project**
   ```bash
   cd c:\Users\BrAiN\Desktop\evaluation_v2
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv venv
   ```

3. **Activate Virtual Environment** (Windows)
   ```bash
   venv\Scripts\activate
   ```

4. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Apply Migrations**
   ```bash
   python manage.py migrate
   ```

6. **Create Superuser (Admin)**
   ```bash
   python manage.py createsuperuser
   ```

7. **Seed Initial Data (Optional)**
   ```bash
   python manage.py seed_levels
   ```

8. **Run Development Server**
   ```bash
   python manage.py runserver
   ```
   Server runs on: `http://127.0.0.1:8000/`

### Project Configuration

**Settings File:** `core/settings.py`
- DEBUG = True (development)
- ALLOWED_HOSTS = [] (development)
- INSTALLED_APPS includes all four custom apps
- Custom AUTH_USER_MODEL = 'accounts.User'
- CSRF_TRUSTED_ORIGINS configured for local development

**Database:**
- Default: SQLite (db.sqlite3)
- Configurable in settings for production (PostgreSQL, MySQL, etc.)

---

## Development Notes

### Project Statistics
- **Total Models:** 13
- **Custom Apps:** 4 (accounts, courses, questions, evaluations)
- **URL Patterns:** 50+
- **Template Files:** 40+
- **Database Tables:** 13+ (including Django built-ins)

### Key Design Decisions

1. **Custom User Model**
   - Allows role-based access control in database
   - Extensible for future user-related features
   - Signals auto-create TeacherProfile when teacher user is created via admin/superuser

2. **TeacherProfile ManyToMany to Departments**
   - Enables teacher assignment to multiple departments
   - Supports cross-departmental teaching

3. **Course → Single Department (Strict FK)**
   - Prevents data inconsistency in rankings
   - Ensures courses appear only in their assigned department rankings
   - Critical for accurate result aggregation

4. **Evaluation Uniqueness Constraint**
   - unique_together = (student, teacher, course)
   - Prevents student from submitting multiple evaluations for same teacher/course
   - Enforces one evaluation per triple

5. **PDF Support Architecture**
   - Separate PDFUpload model for document management
   - Questions linked to source PDF with page/position tracking
   - Enables both manual and PDF-extracted questions

6. **Answer Type Flexibility**
   - Questions can be scored (1-5) or open-text
   - Answers table supports both score and text_answer fields
   - Allows hybrid evaluation forms

### Common Workflows

**Admin Creates Course:**
1. Navigate to `/admin/courses/`
2. Click "New Course"
3. Select department (this determines which department's ranking the course appears in)
4. Select level
5. Optionally select specialization
6. Save course

**Teacher Views Rankings:**
1. Login as teacher
2. Navigate to `/classement/`
3. View public rankings only

**Student Evaluates Teacher:**
1. Navigate to `/evaluate/`
2. Select teacher from list
3. Select course
4. Answer all questions (mix of 1-5 scores and text)
5. Submit evaluation
6. View confirmation page

**Admin Manages Teachers:**
1. Navigate to `/admin/teachers/`
2. Edit teacher: assign to department(s), set name, contact info
3. Toggle teacher: activate/deactivate from system

---

## Developer Handoff

### Purpose
This section gives a future developer the exact starting points to continue work on the project without reverse engineering.

### Core entry points
- `manage.py` — primary Django management entry point
- `core/settings.py` — app registration, custom user model, development configuration
- `core/urls.py` — root URL inclusion for all apps
- `accounts/urls.py` — authentication, profile flow, admin management routes
- `courses/urls.py` — course CRUD routes
- `questions/urls.py` — question/PDF upload routes
- `evaluations/urls.py` — evaluation flow and ranking routes

### Key app responsibilities
- `accounts/` — user model, auth, profiles, admin CRUD for departments/levels/specializations/teachers
- `courses/` — course model, teacher-course assignment, admin course CRUD
- `questions/` — question model and PDF upload/extraction support
- `evaluations/` — student evaluation workflow, answer storage, ranking calculations, PDF generation

### Important conventions
- Teachers are created and managed by admins only; there is no teacher self-registration flow.
- Courses are assigned to exactly one department; department-based ranking depends on this guarantee.
- Student evaluations are unique per `(student, teacher, course)`.
- Questions support both scored and open-answer types in the same `Answer` model.
- Public rankings are department-scoped; teacher department membership is separate from course department assignment.

### Best next steps for new work
1. Identify the feature area in `PROJECT_DOCUMENTATION.md` and corresponding app.
2. Locate the view in `*.py` and the template in `*/templates/*`.
3. Update or extend the URL routing if needed.
4. Run `python manage.py runserver` and verify in browser.
5. Add or update tests in the appropriate app `tests.py`.

### Useful existing files
- `accounts/models.py` — custom `User`, `StudentProfile`, `TeacherProfile`, departments, levels, specializations
- `courses/models.py` — `Course`, `TeacherCourse`
- `evaluations/models.py` — `Evaluation`, `Answer`, `EvaluationPdf`
- `evaluations/views_results.py` — ranking logic and score aggregation
- `accounts/views_admin.py` and `courses/views_admin.py` — admin CRUD logic
- `evaluations/pdf_generator.py` and `evaluations/pdf_converter.py` — PDF utilities

### Setup commands
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### Recommended first fixes
- Confirm teacher dashboard behavior matches the public-only access rule.
- Audit `accounts/views.py` for any teacher creation/profile completion code paths.
- Verify `evaluations/views_results.py` department filtering remains correct.

---

## Known Issues & Fixes

### Issue 1: Courses Appearing in Multiple Department Rankings ✅ FIXED

**Problem:**
- Teacher assigned to two departments
- Course created for Department A only
- Course appeared in rankings for both Department A and B

**Root Cause:**
- `_get_teacher_scores()` function returned ALL courses for teacher regardless of department
- `public_ranking()` view didn't filter results by department when calling `_get_teacher_scores()`

**Solution Applied:**
- Added optional `department` parameter to `_get_teacher_scores(function)`
- Added filter: `if department: query = query.filter(course__department=department)`
- Updated `public_ranking()` view to pass department context (2 call sites fixed)
- Backward compatible: parameter is optional

**File:** `evaluations/views_results.py`
- Lines 242, 245: Updated calls to pass `department=dept`
- Lines 162-170: Added optional department parameter with filtering logic

---

### Issue 2: Low Text Contrast in Dark Theme ✅ FIXED

**Problem:**
- Admin and student dashboards used dark backgrounds with light gray text
- Text contrast ratios failed accessibility standards
- Difficult to read, especially for users with vision impairments

**Root Cause:**
- Dark theme colors: backgrounds #1e293b, #0f172a
- Light gray text: #94a3b8, #64748b
- Insufficient contrast ratio (< 4.5:1 WCAG AA standard)

**Solution Applied:**
- Converted entire UI to light theme
- White backgrounds (#ffffff)
- Dark text (#0f172a, #475569)
- Increased font-weight to 500-700
- Improved button and badge styling for consistency

**Files Modified:**
- `accounts/templates/accounts/base.html` - Base styling
- `accounts/templates/accounts/admin/base_admin.html` - Admin layout
- `accounts/templates/accounts/student_dashboard.html` - Student page
- `evaluations/templates/evaluations/student/base_student.html` - Eval flow
- All admin list/form templates

**Verification:** WCAG AA compliance achieved (contrast > 4.5:1)

---

### Issue 3: Admin Dashboard Top Padding ✅ FIXED

**Problem:**
- Admin dashboard appeared to "hover" in middle of browser with excessive top padding
- User requested: "let it touch the top of the browser"

**Root Cause:**
- `.main` container had `padding: 2rem;` (including top)
- `.admin-layout` and `.admin-toolbar` had margins that pushed content down

**Solution Applied:**
- Changed `.main` padding to `0 2rem 2rem 2rem` (removed top padding)
- Added explicit margin and padding to `.admin-layout` and `.admin-toolbar`
- Admin content now flush with viewport top

**Files Modified:**
- `accounts/templates/accounts/base.html` - Line 58: `.main` padding adjusted
- `accounts/templates/accounts/admin/base_admin.html` - Lines 10-22: layout and toolbar spacing adjusted

**Verification:** Admin dashboard now aligns flush with browser top edge

---

### Issue 4: Emoji in Templates ✅ FIXED

**Problem:**
- 60+ emoji characters scattered across 28+ HTML template files
- Emoji used as decorative stickers in headings, labels, buttons
- Inconsistent, unprofessional appearance

**Root Cause:**
- Manual emoji insertion during template development
- No automated cleanup process

**Solution Applied:**
- Regex Unicode pattern search: `[\u{1F300}-\u{1F6FF}\u{1F900}-\u{1F9FF}\u{1F1E6}-\u{1F1FF}\u{2600}-\u{26FF}\u{2700}-\u{27BF}]`
- Identified all emoji occurrences
- Removed systematically using `apply_patch` tool
- Re-verified with grep search showing 0 remaining matches

**Files Cleaned:** 28+ template files across all apps
- `accounts/templates/accounts/admin/question_list.html`
- `accounts/templates/accounts/admin/level_list.html`
- `accounts/templates/accounts/admin/specialization_list.html`
- `accounts/templates/accounts/admin/course_form.html`
- And 20+ other student/admin template files

**Verification:** Unicode regex search returned 0 matches

---

## Testing Recommendations

### Manual Testing Checklist

- [ ] User registration and login for all three roles
- [ ] Profile completion flow for student and teacher
- [ ] Admin CRUD operations (departments, courses, teachers, etc.)
- [ ] Student evaluation workflow from teacher list to confirmation
- [ ] Public ranking display filters by department correctly
- [ ] Teacher scores view shows only personal courses/departments
- [ ] Course detail pages show individual question scores
- [ ] Light theme renders correctly in Chrome, Firefox, Safari
- [ ] Responsive design on mobile, tablet, desktop breakpoints
- [ ] PDF upload and question extraction (if PDF features used)
- [ ] Permission decorators block unauthorized access
- [ ] Unique constraints prevent duplicate evaluations

### Automated Testing (Future)

Consider adding Django TestCase for:
- Model creation and relationships
- View access control
- Form validation
- Score calculation logic
- Department filtering in rankings

---

## Deployment Checklist

- [ ] Set DEBUG = False
- [ ] Update ALLOWED_HOSTS
- [ ] Generate new SECRET_KEY
- [ ] Configure production database (PostgreSQL recommended)
- [ ] Set up static/media file serving
- [ ] Configure CSRF_TRUSTED_ORIGINS for production domain
- [ ] Run `python manage.py collectstatic`
- [ ] Run `python manage.py migrate` on production database
- [ ] Create production superuser
- [ ] Set up SSL/HTTPS
- [ ] Configure email backend for notifications (if needed)
- [ ] Set up logging and monitoring
- [ ] Backup database regularly
- [ ] Test all functionality in production environment

---

## Support & Troubleshooting

### Common Issues

**Q: "User has no StudentProfile" when student logs in**
A: Student must complete profile first. Redirect to `/complete-profile/student/`

**Q: "Course not appearing in rankings"
A: Verify course is assigned to correct department via `/admin/courses/`

**Q: "Can't see evaluation form"
A: Student must have valid course assignment. Admin must create TeacherCourse entry for teacher/course pair

**Q: "PDF upload fails"
A: Ensure `media/questions_pdfs/` directory exists and is writable

**Q: "Permission denied" on admin pages
A: User must be logged in and have admin role

### Debug Mode

Enable additional logging:
```python
# In settings.py
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'DEBUG',
    },
}
```

---

## Project Timeline & Version History

- **v0.1** - Initial project setup with Django 6.0.6
- **v1.0** - Core models and auth system implemented
- **v1.5** - Evaluation workflow and ranking system added
- **v2.0** - PDF support and results views
- **v2.1** - Light theme UI conversion
- **v2.2** - Bug fixes (department filtering, emoji removal, spacing)
- **Current** - Stable production-ready version with comprehensive documentation

---

## Contact & Support

For questions about project structure or implementation, refer to:
1. This documentation file
2. Inline code comments in view files
3. Django official documentation: https://docs.djangoproject.com/
4. Model `__str__()` methods for debugging relationships

---

**Documentation Generated:** June 2026  
**Last Maintenance:** Latest version  
**Status:** Active Development & Maintenance
