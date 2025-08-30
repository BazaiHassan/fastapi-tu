# Budget Management API Documentation

[![Maktabkhooneh Course](https://img.shields.io/badge/Maktabkhooneh-FastAPI%20Course-blue?logo=book)](https://maktabkhooneh.org/course/%D8%A2%D9%85%D9%88%D8%B2%D8%B4-%D8%B7%D8%B1%D8%A7%D8%AD%DB%8C-%D8%B3%D8%B1%D9%88%DB%8C%D8%B3-fastapi-mk10645/)

## Quick Start

### Clone the Repository
```bash
git clone https://github.com/BazaiHassan/fastapi-tu.git
cd expense-tracker-api
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Run the Server
```bash
fastapi dev core/main.py
```
The API will be available at: `http://localhost:8000`

## Overview
This API provides endpoints for user authentication, expense tracking, category management, and budget planning. The API follows RESTful principles and uses JSON for data exchange.

## Base URL
All endpoints are relative to the base URL of your API deployment.

## Authentication
Most endpoints require authentication using JWT tokens. The authentication flow is:

1. Register a new user account
2. Login to receive an access token
3. Include the token in subsequent requests as a Bearer token in the Authorization header

## Endpoints

### User Management

#### Register User
```http
POST /api/v1/user/register
```
Creates a new user account.

**Request Body:**
```json
{
  "email": "string",
  "password": "string",
  "first_name": "string",
  "last_name": "string",
  "phone_number": "string | null",
  "default_currency": "string | null (default: USD)",
  "language": "string | null (default: en)",
  "timezone": "string | null (default: UTC)",
  "country": "string | null",
  "date_of_birth": "string | null"
}
```

**Response:**
- 200: Successful registration

#### Login
```http
POST /api/v1/user/login
```
Authenticates a user and returns access tokens.

**Request Body:**
```json
{
  "email": "string",
  "password": "string"
}
```

**Response:**
```json
{
  "access_token": "string",
  "token_type": "string"
}
```

#### Refresh Token
```http
POST /api/v1/user/refresh
```
Refreshes the authentication token.

**Response:**
```json
{
  "access_token": "string",
  "token_type": "string"
}
```

#### Get Current User
```http
GET /api/v1/user/current
```
Returns information about the currently authenticated user.

#### Logout
```http
POST /api/v1/user/logout
```
Invalidates the current user's authentication token.

#### Forgot Password
```http
POST /api/v1/user/forget-password?email=string
```
Initiates a password reset process for the user with the specified email.

### Expense Management

#### Get Expense List
```http
GET /api/v1/expense/list
```
Retrieves a list of expenses for the authenticated user.

### Category Management

#### Get Category List
```http
GET /api/v1/category/list
```
Retrieves a list of available categories.

### Budget Management

#### Get Budget List
```http
GET /api/v1/budget/list
```
Retrieves a list of budgets for the authenticated user.

**Response:**
```json
[
  {
    "id": "uuid",
    "amount": "string",
    "period": "string",
    "start_date": "date-time",
    "end_date": "date-time",
    "category_id": "uuid | null",
    "user_id": "uuid",
    "created_at": "date-time"
  }
]
```

#### Add Budget
```http
POST /api/v1/budget/add
```
Creates a new budget.

**Request Body:**
```json
{
  "amount": "number > 0",
  "period": "string (1-20 characters)",
  "start_date": "date-time",
  "end_date": "date-time",
  "category_id": "uuid | null",
  "user_id": "uuid"
}
```

**Response:**
```json
{
  "id": "uuid",
  "amount": "string",
  "period": "string",
  "start_date": "date-time",
  "end_date": "date-time",
  "category_id": "uuid | null",
  "user_id": "uuid",
  "created_at": "date-time"
}
```

#### Update Budget
```http
PUT /api/v1/budget/update/{budget_id}
```
Updates an existing budget.

**Path Parameters:**
- `budget_id`: UUID of the budget to update

**Request Body:**
```json
{
  "amount": "number > 0 | null",
  "period": "string (1-20 characters) | null",
  "category_id": "uuid | null",
  "start_date": "date-time | null",
  "end_date": "date-time | null"
}
```

**Response:**
```json
{
  "id": "uuid",
  "amount": "string",
  "period": "string",
  "start_date": "date-time",
  "end_date": "date-time",
  "category_id": "uuid | null",
  "user_id": "uuid",
  "created_at": "date-time"
}
```

#### Delete Budget
```http
DELETE /api/v1/budget/delete/{budget_id}
```
Deletes a budget.

**Path Parameters:**
- `budget_id`: UUID of the budget to delete

## Error Handling

The API returns standard HTTP status codes:

- 200: Success
- 422: Validation error

Validation errors follow this format:
```json
{
  "detail": [
    {
      "loc": ["array of strings or integers"],
      "msg": "string",
      "type": "string"
    }
  ]
}
```

## Data Types

- **uuid**: Universally unique identifier
- **date-time**: ISO 8601 formatted datetime string
- **string**: UTF-8 encoded text

## Rate Limiting
The API may implement rate limiting to prevent abuse. Check response headers for rate limit information.

## Support
For support regarding this API, please contact the development team.
