# VERSEWISE-CMS Backend

This document provides instructions on how to set up and run the Versewise CMS backend either by creating a virtual environment or using Docker.

## Prerequisites

- Python 3.8 or higher
- pip package manager
- Docker (optional)

## Running with Virtual Environment

1. **Clone the repository:**

    ```bash
    git clone https://github.com/VerseWise/verse-wise-cms.git
    cd verse-wise-cms/backend
    ```

2. **Create a virtual environment:**

    ```bash
    python3 -m venv env
    ```

3. **Activate the virtual environment:**

    - On Windows:

        ```bash
        .\env\Scripts\activate
        ```

    - On macOS/Linux:

        ```bash
        source env/bin/activate
        ```

4. **Install the dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

5. **Set Up Environment Variables:**
    Copy .env.example to .env
    ```bash
    cp .env.example .env
    ```
    Open the `.env` file in a text editor and update the values as needed.

6. **Run the application:**

    ```bash
    python3 run.py
    ```

## Running with Docker

1. **Clone the repository:**

    ```bash
    git clone https://github.com/VerseWise/verse-wise-cms.git
    cd verse-wise-cms/backend
    ```

2. **Set Up Environment Variables:**
    Copy .env.example to .env
    ```bash
    cp .env.example .env
    ```
    Open the `.env` file in a text editor and update the values as needed.

3. **Build the Docker image:**

    ```bash
    docker build --network=host -t versewise-cms-backend .
    ```

4. **Run the Docker container:**

    ```bash
    docker run -p 5000:5000 versewise-cms-backend
    ```

## Running with Docker Compose

1. **Clone the repository:**

    ```bash
    git clone https://github.com/VerseWise/verse-wise-cms.git
    cd verse-wise-cms/backend
    ```

2. **Set Up Environment Variables:**

    Copy `.env.example` to `.env`:

    ```bash
    cp .env.example .env
    ```

    Open the `.env` file in a text editor and update the values as needed.

3. **Run the application with Docker Compose:**

    ```bash
    docker-compose up
    ```

4. **Access the Application:**

    Once the application is running, you can access it at `http://localhost:5000`.

## Accessing the Application

Once the application is running, you can access it at `http://localhost:5000`.

## API Endpoints

### Authentication

- **POST /login**
  - Description: Authenticates a user and returns a token.
  - Request Body: `{ "username": "testuser", "password": "testpassword" }`

- **POST /register**
  - Description: Registers a new user.
  - Request Body: `{ "username": "testuser", "first_name": "testname", "middle_name": "testmiddle", "last_name": "testlast", "email": "test@email.com", "phone_number": "test_phone", "password": "testpassword" }`

### Users

- **GET /users**
  - Description: Retrieves a paginated list of all users (Only accessible by admins).

- **GET /users/{id}**
  - Description: Retrieves details of a specific user (Only accessible by admins and the concerned user).

- **POST /users**
  - Description: Creates a new user with desired role (Only accessible by admins).
  - Request Body: `{ "username": "testuser7", "first_name": "testname", "middle_name": "testmiddle", "last_name": "testlast", "email": "test7@email.com", "phone_number": "test_phone", "password": "testpassword", "role": "admin" }`

- **PUT /users/{id}**
  - Description: Promotes non-admin users to editor or admin (Only accessible by admins).
  - Request Body: `{ "role": "admin" }`

- **DELETE /users/{id}**
  - Description: Deletes a user account (Only accessible by admins and the concerned user).

### Contents

- **GET /contents**
  - Description: Retrieves a paginated list of all content items (Accessible by everyone).

- **GET /contents/{id}**
  - Description: Retrieves details of a specific content (Accessible by everyone).

- **POST /contents**
  - Description: Creates a new content item (Only accessible by admins and editors).
  - Request Body: `{ "title": "Title", "content": "Content body" }`

- **PUT /contents/{id}**
  - Description: Edits content properties. It can accept only the value to be edited (Only accessible by admins and editors).
  - Request Body: `{ "content": " Updated Content body" }`

- **DELETE /contents/{id}**
  - Description: Deletes a content item (Only accessible by admins and editors).
