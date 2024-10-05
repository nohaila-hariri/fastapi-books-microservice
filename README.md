# FastAPI Microservice for Managing Books

This project is a microservice built with **FastAPI** that provides a simple RESTful API to manage a list of books. It integrates **MongoDB** using the **Motor** library for asynchronous database operations, and the entire setup is containerized using **Docker** and **Docker Compose**.

## Features

- **GET /books**: Retrieve all books
- **GET /books/{book_id}**: Retrieve a specific book by ID
- **POST /books**: Add a new book
- **PUT /books/{book_id}**: Update an existing book
- **DELETE /books/{book_id}**: Delete a book

## Technologies Used

- **FastAPI**: For building the web API
- **Motor**: Asynchronous MongoDB driver
- **MongoDB**: Database for storing books
- **Docker**: To containerize the application
- **Docker Compose**: To manage multiple services, including FastAPI and MongoDB

## Prerequisites

Make sure you have the following installed on your machine:

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Installation

### 1. Clone the repository

```bash
git clone <repository-url>
cd fastapi-microservice
```

### 2. Create and build the Docker containers

To create and build the Docker containers for your FastAPI microservice and MongoDB, use the following command with Docker Compose:

```bash
docker-compose up --build
```
Once the containers are running, you can access the FastAPI application at http://localhost:8000.

### 3. Access the API

Once the services are up and running, the API will be available at: [api](http://localhost:8000)

### Project Structure

fastapi-microservice/ 
├── app/ 
│ ├── main.py # FastAPI app with endpoints 
│ ├── models.py # Models used in the application 
│ ├── schemas.py # Pydantic schemas 
│ └── database.py # MongoDB connection configuration 
├── Dockerfile # Docker image setup 
├── docker-compose.yml # Docker Compose setup 
├── requirements.txt # Python dependencies
├── .env # env variable used in this project
└── README.md # Project documentation

### Notes

- The MongoDB service is linked to the FastAPI app through the `docker-compose.yml` file.
- Data will be stored in a Docker volume (`mongo_data`) to persist between container restarts.
