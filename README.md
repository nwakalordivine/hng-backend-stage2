# HNG Stage 1: String Analyzer Service

This is a RESTful API built with **FastAPI** for the HNG Internship Stage 1 task. The service analyzes a given string, computes its properties, stores them in a **Neon (PostgreSQL)** database, and provides multiple endpoints for creating, retrieving, and filtering the data.

This project uses **SQLAlchemy** for asynchronous database operations and **Alembic** for handling database migrations.

---

## 🚀 Live Endpoint

*(Remember to add your live deployment URL here once you host it!)*

**Live API URL:** `[Your-Deployment-URL-Here]`

---

## ✨ Features

- **String Analysis**: Computes length, palindrome status (case-insensitive), unique character count, word count, SHA256 hash, and a full character frequency map.
- **Persistent Storage**: All analysis is stored in a serverless PostgreSQL database (Neon) using SQLAlchemy's async engine.
- **Database Migrations**: Uses Alembic to manage database schema changes safely.
- **CRUD Operations**: Full Create, Read, and Delete functionality for analyzed strings.
- **Advanced Filtering**:
    - `GET /strings`: A powerful filtering endpoint to query strings by their properties (e.g., `is_palindrome`, `min_length`, `word_count`).
    - `GET /strings/filter-by-natural-language`: A smart endpoint that parses simple English queries (e.g., "all single word palindromic strings") into database filters.
- **Error Handling**: Provides clear error messages for conflicts (`409`), missing resources (`404`), and bad requests (`400` / `422`).
- **Interactive API Docs**: Automatic, detailed API documentation with Swagger UI (`/docs`) and ReDoc (`/redoc`).

---

## 🛠️ Technology Stack

- **Framework**: FastAPI
- **Database**: Neon (Serverless PostgreSQL)
- **ORM**: SQLAlchemy (with `asyncio` support)
- **Database Driver**: `asyncpg` (async) & `psycopg2-binary` (for Alembic)
- **Migrations**: Alembic
- **Server**: Uvicorn
- **Data Validation**: Pydantic
- **Environment**: `pydantic-settings`

---

## 🚀 Getting Started

Follow these instructions to get a local copy up and running for development and testing.

### Prerequisites

You'll need the following installed:
- **Python 3.10+**
- **Git**

You'll also need an account with:
- **[Neon](https://neon.tech/)**: To create your free serverless PostgreSQL database.

### 1. Installation & Setup

1.  **Clone the repository:**
    ```bash
    git clone <your-repository-url>
    cd string-analyzer-api
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    source venv/Scripts/activate  # On Windows
    # source venv/bin/activate    # On macOS/Linux
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

### 2. Configure Environment Variables

1.  Create a `.env` file in the root directory.
2.  Log in to Neon, create a project, and get your connection string.
3.  Add it to your `.env` file. **Note:** Use `ssl=require` for the `asyncpg` driver.

    ```.env
    # .env file
    # Replace with your own Neon DB connection string
    DATABASE_URL="postgresql+asyncpg://user:password@host.neon.tech/dbname?ssl=require"
    ```

### 3. Run Database Migrations

This project uses Alembic to manage the database schema.

1.  **Configure Alembic:**
    - Open the `alembic.ini` file.
    - Find the line `sqlalchemy.url = ...`
    - Copy your `DATABASE_URL` from `.env` and paste it here, but **change the driver** from `asyncpg` to `psycopg2` and `ssl=` to `sslmode=`. This is required for Alembic's synchronous operations.
    - **Example `alembic.ini`:**
      ```ini
      sqlalchemy.url = postgresql+psycopg2://user:password@host.neon.tech/dbname?sslmode=require
      ```

2.  **Apply the migrations:**
    Run the following command to create the `analyzed_strings` table in your Neon database:
    ```bash
    alembic upgrade head
    ```

### 4. Run the Application

You're all set! Run the server with Uvicorn:

```bash
uvicorn app.main:app --reload