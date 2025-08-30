# Company Management System API

![Build Status](https://img.shields.io/badge/build-passing-brightgreen)
![Python Version](https://img.shields.io/badge/python-3.11-blue)
![Django Version](https://img.shields.io/badge/django-5.2-darkgreen)
![License](https://img.shields.io/badge/license-MIT-lightgrey)

A robust and scalable RESTful API built with Django and Django REST Framework to manage companies, departments, employees, projects, and employee performance review cycles. The system is containerized with Docker and includes a full production-ready stack with PostgreSQL.

---

## 1. Core Features

This platform provides a comprehensive backend solution for company management with a focus on modularity, security, and maintainability.

### ✅ Mandatory Requirements Checklist

-   [x] **CRUD for Company:** Full create, read, update, and delete operations.
-   [x] **CRUD for Department:** Full create, read, update, and delete operations.
-   [x] **CRUD for Employee:** Full create, read, update, and delete operations.
-   [x] **Data Models:** All required data models (`User`, `Company`, `Department`, `Employee`) implemented with specified fields.
-   [x] **Auto-Calculated Fields:** Denormalized counters on models are automatically updated.
-   [x] **Employee Performance Review Workflow:** A state machine manages the full review cycle (`Pending` -> `Scheduled` -> `Approved`/`Rejected`).
-   [x] **Security & Permissions:** Implemented robust Role-Based Access Control (RBAC) for `Admin`, `Manager`, and `Employee` roles.
-   [x] **Secure Authentication:** Uses JSON Web Token (JWT) for secure, stateless authentication.
-   [x] **RESTful API:** Follows REST conventions with proper HTTP methods and status codes.
-   [x] **Enhanced Admin Interface:** Includes a modern, user-friendly admin panel powered by `django-jazzmin`.
-   [ ] **Unit & Integration Tests:** (Project structure is set up, but test cases are not yet implemented).

### ✨ Bonus Requirements Checklist

-   [x] **CRUD for Project:** Full create, read, update, and delete operations for projects.
-   [x] **Production-Grade Logging:** Implemented a rotating file logger to track application behavior and capture errors without consuming disk space.

---

## 2. Architectural & Technical Decisions

This project was built with a production environment in mind, emphasizing best practices for scalability and maintainability.

-   **Modular App Structure:** The project is logically divided into four Django apps (`users`, `organization`, `projects`, `performance`). This **Separation of Concerns** makes the codebase easier to navigate, test, and scale independently.

-   **Data Denormalization & Consistency:** For performance, fields like `number_of_employees` are stored directly on the model. To ensure these counters are **always accurate**, **Django Signals** (`post_save`, `post_delete`) are used to automatically increment/decrement the values when related objects are created or deleted.

-   **Role-Based Access Control (RBAC):** Security is enforced using custom DRF Permission Classes. User roles (`Admin`, `Manager`, `Employee`) are defined on the `User` model, and these classes check the user's role to grant or deny access to specific API endpoints and actions.

-   **State Management with `django-fsm`:** The Employee Performance Review workflow is managed as a **Finite State Machine**. This library enforces the allowed transitions between stages (e.g., a review cannot be `Approved` directly from `Pending`), ensuring the business logic is followed.

-   **Efficient Pagination:** The API uses **Cursor Pagination** ordered by `created_at`. This is significantly more performant for large datasets than traditional offset/limit pagination, as it avoids slow `COUNT` queries and provides a stable ordering.

-   **Production-Ready Logging:** The configuration uses a `RotatingFileHandler` to prevent log files from growing indefinitely. It separates logs into an `app.log` for general information and an `error.log` for critical errors with stack traces.

-   **Configuration Management:** All sensitive keys and environment-specific settings are managed outside of version control in a `.env` file, loaded securely using `python-decouple`.

---

## 3. Tech Stack

| Component         | Technology / Library                                       |
| ----------------- | ---------------------------------------------------------- |
| **Backend** | Python 3.11, Django, Django REST Framework               |
| **Database** | PostgreSQL                                                 |
| **Authentication**| Django REST Framework Simple JWT                           |
| **State Machine** | `django-fsm`                                               |
| **API Docs** | `drf-spectacular` (OpenAPI 3 / Swagger UI)                 |
| **Admin Interface** | `django-jazzmin`                                           |
| **Configuration** | `python-decouple`                                          |
| **Environment** | Docker & Docker Compose                                    |
| **Testing** | Pytest                                                     |

---

## 4. 🚀 Getting Started

The entire application stack is containerized using Docker, allowing for a simple and consistent setup process.

### Prerequisites

-   Docker
-   Docker Compose

### Installation & Setup

1.  **Clone the Repository**
    ```bash
    git clone [https://github.com/mostafa20220/company-management.git](https://github.com/mostafa20220/company-management-system.git)
    cd company-management
    ```

2.  **Create an Environment File**
    Create a file named `.env` by copying the example. The defaults are ready for local development.
    ```bash
    cp .env.example .env
    ```

3.  **Build and Run with Docker Compose**
    This command will build the Django image and start containers for the web app and PostgreSQL database.
    ```bash
    docker-compose up --build
    ```
    The API will now be running at `http://localhost:8000`.

4.  **Create a Superuser (Admin)**
    In a new terminal window, run the following command to create an admin account.
    ```bash
    docker-compose exec django python manage.py createsuperuser
    ```

---

## 5. API Documentation

The API is fully documented using the OpenAPI 3 standard, with an interactive Swagger UI.

-   **Swagger UI:** `http://localhost:8000/api/v1/docs/`

### Authentication

To access protected endpoints, first obtain a JWT token from the `/api/v1/auth/login/` endpoint. Then, include the token in the `Authorization` header of your requests with the `JWT` prefix.

**Example:** `Authorization: JWT <your_access_token>`

---

## 6. Security Measures Implemented

-   **JWT Authentication:** All sensitive endpoints are protected and require a valid JSON Web Token with configurable expiration times.
-   **Role-Based Authorization:** Granular permissions ensure that users can only access or modify data appropriate for their role.
-   **Explicit Serializer Fields:** The API uses explicit field declarations in serializers instead of `fields = "__all__"` to prevent accidentally exposing sensitive model fields.
-   **Environment Variables:** All sensitive information (like `SECRET_KEY` and database credentials) is managed via a `.env` file and is not hardcoded.
-   **CSRF Protection:** Configured with trusted origins for web-based interactions.

---
