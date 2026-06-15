# Evaluation System - UML Diagrams

## 1. Class Diagram

The core data model showing all entities and their relationships.

```mermaid
classDiagram
    class User {
        +int id
        +str username
        +str email
        +str first_name
        +str last_name
        +str role (admin, teacher, student)
        +bool is_active
        +datetime created_at
        +is_admin()
        +is_teacher()
        +is_student()
        +has_completed_profile()
    }

    class StudentProfile {
        +int id
        +OneToOne user
        +Foreign department
        +Foreign level
        +Foreign specialization
    }

    class TeacherProfile {
        +int id
        +OneToOne user
        +Foreign department
    }

    class Department {
        +int id
        +str name
        +str description
        +datetime created_at
        +datetime updated_at
    }

    class Specialization {
        +int id
        +str name
        +Foreign department
        +str description
        +datetime created_at
        +datetime updated_at
    }

    class Level {
        +int id
        +str name
        +int order
    }

    class Course {
        +int id
        +str name
        +str description
        +Foreign department
        +Foreign level
        +Foreign specialization
        +bool is_general
        +bool is_active
        +datetime created_at
        +datetime updated_at
    }

    class TeacherCourse {
        +int id
        +Foreign teacher
        +Foreign course
        +datetime created_at
    }

    class Question {
        +int id
        +str text
        +str type (scored, open)
        +bool is_active
        +Foreign source_pdf
        +int pdf_page
        +int position
        +datetime created_at
        +datetime updated_at
    }

    class PDFUpload {
        +int id
        +File file
        +str original_filename
        +Foreign uploaded_by
        +datetime created_at
    }

    class Evaluation {
        +int id
        +Foreign student
        +Foreign teacher
        +Foreign course
        +str status (pending, submitted)
        +datetime created_at
        +datetime updated_at
    }

    class Answer {
        +int id
        +Foreign evaluation
        +Foreign question
        +int score
        +str text_answer
        +datetime created_at
    }

    class EvaluationPdf {
        +int id
        +OneToOne evaluation
        +str file_path
        +datetime generated_at
    }

    %% Relationships
    User "1" -- "0..1" StudentProfile : has
    User "1" -- "0..1" TeacherProfile : has
    User "1" -- "*" TeacherCourse : teaches
    User "1" -- "*" Evaluation : evaluates
    User "1" -- "*" Evaluation : is_evaluated
    User "1" -- "*" PDFUpload : uploads

    StudentProfile "*" -- "1" Department : belongs_to
    StudentProfile "*" -- "1" Level : enrolled_in
    StudentProfile "*" -- "1" Specialization : specializes_in

    TeacherProfile "*" -- "1" Department : works_in

    Department "1" -- "*" Specialization : contains
    Department "1" -- "*" Course : offers

    Specialization "0..1" -- "*" Course : includes

    Level "1" -- "*" Course : groups

    Course "1" -- "*" TeacherCourse : assigned_to
    Course "1" -- "*" Evaluation : evaluated_in

    PDFUpload "1" -- "*" Question : contains

    Evaluation "1" -- "*" Answer : has
    Evaluation "1" -- "0..1" EvaluationPdf : generates

    Answer "*" -- "1" Question : answers
```

---

## 2. Sequence Diagram

The workflow of a student completing an evaluation.

```mermaid
sequenceDiagram
    participant Student
    participant System as Django System
    participant DB as Database
    participant PDFGenerator as PDF Generator

    Student->>System: Login (student@example.com)
    System->>DB: Validate credentials
    DB-->>System: User found
    System-->>Student: Authenticated / Dashboard

    Student->>System: View pending evaluations
    System->>DB: Query evaluations (status=pending)
    DB-->>System: Return pending evaluations
    System-->>Student: Display pending list

    Student->>System: Click "Start Evaluation" for Teacher A
    System->>DB: Fetch evaluation with questions
    DB-->>System: Return Evaluation + Questions
    System-->>Student: Display evaluation form

    loop For each question
        Student->>Student: Read question
        alt Question type = scored
            Student->>System: Select score (1-5)
        else Question type = open
            Student->>System: Enter text answer
        end
    end

    Student->>System: Submit evaluation
    System->>DB: Validate all answers
    DB-->>System: Validation passed
    System->>DB: Create Answer records
    DB-->>System: Answers saved
    System->>DB: Update Evaluation status to submitted
    DB-->>System: Status updated

    System->>PDFGenerator: Generate evaluation PDF
    PDFGenerator->>DB: Fetch evaluation & answers
    DB-->>PDFGenerator: Return data
    PDFGenerator->>PDFGenerator: Generate PDF file
    PDFGenerator->>System: PDF created
    System->>DB: Create EvaluationPdf record
    DB-->>System: Record created

    System-->>Student: Evaluation submitted + PDF link
    Student->>System: Download PDF
    System-->>Student: PDF file
```

---

## 3. Use Case Diagram

The actors and their interactions with the system.

```mermaid
graph TB
    subgraph Actors
        Admin["👨‍💼 Admin"]
        Teacher["👨‍🏫 Teacher"]
        Student["👨‍🎓 Student"]
    end

    subgraph StudentUseCases["Student Use Cases"]
        SUC1["Register / Login"]
        SUC2["Complete Profile"]
        SUC3["View Pending Evaluations"]
        SUC4["Answer Evaluation"]
        SUC5["Submit Evaluation"]
        SUC6["Download Evaluation PDF"]
        SUC7["View Evaluation Results"]
    end

    subgraph TeacherUseCases["Teacher Use Cases"]
        TUC1["Login"]
        TUC2["View Assigned Courses"]
        TUC3["View Student Evaluations"]
        TUC4["View Ranking/Statistics"]
    end

    subgraph AdminUseCases["Admin Use Cases"]
        AUC1["Manage Departments"]
        AUC2["Manage Specializations"]
        AUC3["Manage Levels"]
        AUC4["Manage Courses"]
        AUC5["Manage Teachers"]
        AUC6["Manage Questions"]
        AUC7["Manage Evaluations"]
        AUC8["Upload Question PDFs"]
    end

    Student -.-> SUC1
    Student -.-> SUC2
    Student -.-> SUC3
    Student -.-> SUC4
    Student -.-> SUC5
    Student -.-> SUC6
    Student -.-> SUC7

    Teacher -.-> TUC1
    Teacher -.-> TUC2
    Teacher -.-> TUC3
    Teacher -.-> TUC4

    Admin -.-> AUC1
    Admin -.-> AUC2
    Admin -.-> AUC3
    Admin -.-> AUC4
    Admin -.-> AUC5
    Admin -.-> AUC6
    Admin -.-> AUC7
    Admin -.-> AUC8

    SUC1 -.includes.-> SUC2
    SUC4 -.includes.-> SUC5
    SUC5 -.includes.-> SUC6
```

---



---

## 4. Deployment Diagram

Architecture and deployment of the application.

```mermaid
graph TB
    subgraph Client["Client Layer"]
        Web["🌐 Web Browser"]
        AdminClient["👨‍💼 Admin Interface"]
        StudentClient["👨‍🎓 Student Portal"]
        TeacherClient["👨‍🏫 Teacher Dashboard"]
    end

    subgraph Application["Application Layer"]
        Django["Django 6.0.6 Server"]
        AuthModule["Authentication Module"]
        EvalModule["Evaluation Module"]
        QuestModule["Questions Module"]
        CourseModule["Course Module"]
        PDFGen["PDF Generator/Converter"]
    end

    subgraph Services["External Services"]
        ReportLab["ReportLab 4.5.1 (PDF Gen)"]
        PyPDF2["PyPDF2 3.0.1 (PDF Parse)"]
    end

    subgraph DataLayer["Data Layer"]
        MySQL["MySQL Database"]
        FileStorage["File Storage"]
        MediaDir["Media/Evaluations/"]
        QuestionsDir["Questions PDFs/"]
    end

    Web -.->|HTTP/HTTPS| Django
    AdminClient -.->|Admin Routes| Django
    StudentClient -.->|Student Routes| Django
    TeacherClient -.->|Teacher Routes| Django

    Django -.-> AuthModule
    Django -.-> EvalModule
    Django -.-> QuestModule
    Django -.-> CourseModule
    Django -.-> PDFGen

    PDFGen -.-> ReportLab
    PDFGen -.-> PyPDF2

    EvalModule -.-> MySQL
    QuestModule -.-> MySQL
    CourseModule -.-> MySQL
    AuthModule -.-> MySQL

    PDFGen -.-> FileStorage
    FileStorage -.-> MediaDir
    FileStorage -.-> QuestionsDir

    EvalModule -.->|Store PDFs| MediaDir
    QuestModule -.->|Store Upload| QuestionsDir

    style Client fill:#e1f5ff
    style Application fill:#fff3e0
    style Services fill:#f3e5f5
    style DataLayer fill:#e8f5e9
```

