# To-Do List Backend

This is the backend for a To-Do List application, built using Python, FastAPI, and MongoDB. It provides endpoints for user authentication, task management, profile management, and more.

---

## Features

### 1. **Authentication**

- **Signup:** Create a new user account.
- **Login:** Authenticate users with email and password.
- **Forgot Password:** Request a password reset email.
- **New Password:** Set a new password after receiving the reset link.

### 2. **To-Do List**

- **Create:** Add a new task.
- **All:** Retrieve all tasks.
- **Get by ID:** Fetch a specific task using its ID.
- **Soft Delete:** Mark a task as deleted without removing it permanently.
- **Update:** Modify task details.
- **Delete:** Permanently remove a task.
- **Get Recently Deleted:** List tasks that were recently soft-deleted.
- **Patch Recently Deleted:** Restore or permanently delete recently soft-deleted tasks.

### 3. **Profile**

- **Get Information** Get user profile information.
- **Reset Password:** Change the password for an authenticated user.
- **Update Profile:** Edit user profile information.

---

## Project Structure

```bash

  | __src
  |     |__core # .env Config
  |     |__db # Database Config
  |     |__middleware # Middleware  
  |     |__models # Database models and schemas
  |     |__routes # API endpoints
  |     |__schemas
  |     |__services # Core business logic
  |     |__utils
  |
  |___main.py # Entry point of the application
  |__.dockerignore
  |__.env
  |__.env.example
  |__docker-compose.yml
  |__Dockerfile
  |__requirements.tex # Python dependencies
  |__README.md # Project documentation
  |

```

## Installation and Setup

### Prerequisites

- Python 3.12 or higher
- MongoDB instance (local or cloud-based)

### Steps

```bash
  python -m venv venv

  source venv/bin/activate  # On Windows: .venv\scripts\activate.ps1   

  pip install -r requirements.txt 

```

### Run the application

```bash

  uvicorn main:app --reload

```

### Access the API documentation

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## Environment Variables

> .env

To run this project, you will need to add the following environment variables to your .env file

```bash

  DB_URL=<your_mongo_uri>
  DB_NAME=<your_mongo_collection>

  SECRET_KEY=<your_jwt_secret>
  ALGORITHM=<your_jwt_secret>

  MAIL_PASSWORD=<your_mail_password>
  MAIL_SERVER=<your_mail_server>
  MAIL_PORT=<your_mail_port>
  MAIL_USERNAME=<your_mail_username or email>

```

## API Endpoints Overview

### Authentication

| Endpoint | Method     | Description                |
| :-------- | :------- | :------------------------- |
| `/auth/signup` | `POST` | Register a new user     |
| `/auth/signup` | `POST` | Authenticate a user     |
| `/auth/forgot-password` | `POST` | Request password reset email |
| `/auth/new-password` | `POST` | Set a new password |

### To-Do List

| Endpoint | Method     | Description                |
| :-------- | :------- | :------------------------- |
| `/todo/create` | `POST` | Create a new task     |
| `/todo/all` | `GET` | Get all tasks     |
| `/todo/get/{id}` | `GET` | Get a task by ID |
| `/todo/soft-delete/{id}` | `PATCH` | Soft-delete a task |
| `/todo/update/{id}` | `PUT` | Update a task |
| `/todo/delete` | `DELETE` | Permanently delete a task |
| `/todo/recently-deleted` | `GET` | Get recently deleted tasks |
| `/todo/recently-deleted` | `PATCH` | Restore or delete recently deleted tasks |

### Profile

| Endpoint | Method     | Description                |
| :-------- | :------- | :------------------------- |
| `/profile` | `GET` | profile information     |
| `/profile/reset-password` | `PATCH` | Reset the password     |
| `/profile/update` | `PUT` | Update user profile |

## License

This project is licensed under the MIT License. See the LICENSE file for details.
