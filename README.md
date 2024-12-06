# Todo List API

Simple solution for [Todo List API](https://roadmap.sh/projects/todo-list-api) challenge.

## Introduction

This project is a Todo-list API built with flask, using PostgreSQL as database. It leverages SQLAlchemy for ORM and Alembic for database migrations. It includes user authentication using JWT(Json Web Tokens) and password hashing for secure login. The API supports user registration, login, task management(CRUD), status-based filtering, and pagination.

## Features

- Provide functionality for user registration and login(JWT).
- Logged-in users can create, read, update and delete tasks.
- Users can filter tasks by their status (e.g., todo, in-progress, or done).
- User can specify a page to retrive tasks.

## API Endpoints

### User Route

- **GET**/user/register: To register an account with name, email and password.
- **POST**/user/login: To log into the task manager.

### Task Route

- **GET**/task/myTask: Get all task information.
- **GET**/task/myTask/status: Get tasks with specified status.
- **POST**/task/add: Add new task with a description and status.
- **PATCH**/task/update/id: Update the status of the task with the provided id.
- **DELETE**/task/delete/id: Delete the task with the given id.

### Pagination

By Using pagination, users can select a specific page and limit the number of tasks displayed per page.

```shell
# Retrieve tasks from page 1, with 10 task per page.
http://localhost:8080/task/myTask?page=1&limit=10
```

## Installation

To get started with this project, clone the repository to your local machine:

```shell
# Clone the repository
git clone https://github.com/HsinLing-Chang/Todo-List-API.git

# Navigate into the cloned project directory
cd Todo-List-API

# Run the Python script
python app.py
```

## Setting Up Environment Variables

1. Create a `.env`file in the root directory of the project if it doesn’t exist.
2. Add the `Secret` and `DATABASE_URL` Configuration to the `.env` file as follow.

- The `Secret` is used for both signing (encrypting) and verifying (decrypting) the JWT tokens.

- The `DATABASE_URL` is used to configure the connection between SQLAlchemy and the database.
  ```shell
  SECRET = "User secret"
  DATABASE_URL = "postgresql://username:password@host:port/database_name"
  ```

## Structure

1. **User**

```json
{
  "id": 1,
  "username": "User name",
  "email": "example@gmail.com",
  "password": "password"
}
```

2. **Task**

```json
{
    "id":1,
    "user_email": "user_email"
    "description": "Take my dog for a walk.",
    "status": "todo",
    "createAt":"Wed, 27 Nov 2024 19:49:19 GMT",
    "updateAt":"Sun, 01 Dec 2024 19:09:19 GMT",
}
```
