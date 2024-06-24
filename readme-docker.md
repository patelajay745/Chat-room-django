# StudyRoom Project

This is the README for running the StudyRoom project using Docker.

## Prerequisites

- Docker installed on your machine
- Docker Compose installed (optional, if using Compose)

## Setup and Run

Follow these steps to set up and run the StudyRoom project with Docker.

### Step 1: Create a Docker Network

Create a Docker network to allow communication between containers.

```bash
docker network create my-network
```

### Step 2: Run PostgreSQL Container

Run the PostgreSQL container with the specified environment variables.

```
docker run --name my-postgres \
 -p 5432:5432 \
 -e POSTGRES_USER='postgres' \
 -e POSTGRES_PASSWORD='0745' \
 --network my-network \
 -d postgres
```

### Step 3: Initialize the Database

Access the PostgreSQL container and create the database.

```bash
docker exec -it my-postgres bash

psql -U postgres

CREATE DATABASE studyroom OWNER postgres;

\q

exit
```

### Step 4: Build the StudyRoom Docker Image

Build the Docker image for the StudyRoom project.

```bash
docker build -t studyroom .
```

### Step 5: Run the StudyRoom Container

Run the StudyRoom container with the necessary environment variables.

```bash
docker run --name my-studyroom-c1 \
 -p 8000:8000 \
 -e DB_NAME='studyroom' \
 -e DB_USER='postgres' \
 -e DB_USER_PASSWORD='0745' \
 -e DB_HOST='my-postgres' \
 -e DB_PORT='5432' \
 -e AWS_ACCESS_KEY_ID='' \
 -e AWS_SECRET_ACCESS_KEY='' \
 -e AWS_STORAGE_BUCKET_NAME='' \
 -e SE_S3='' \ #if you want s3 as backend provide TRUE
 --network my-network \
 -d studyroom
```

### Step 6: Apply Database Migrations

Access the StudyRoom container and apply the database migrations.

```bash
docker exec -it my-studyroom-c1 python manage.py migrate
```

### Accessing the Application

Once the containers are running and migrations are applied, you can access the StudyRoom application at:

http://localhost:8000
