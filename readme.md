# FastAPI with ScyllaDB

This is a simple FastAPI project using ScyllaDB. Everything is running on Docker and Docker Compose.

## Requirements

- Docker
- Docker Compose

## Setup

1. Clone the repository:
    ```sh
    git clone https://github.com/riishiiiii/scylladb-fastapi-crud.git
    cd scylladb-fastapi-crud
    ```

2. Start the services:
    ```sh
    docker-compose up --build
    ```

3. Access the FastAPI application:
    Open your browser and navigate to `http://localhost:8000/docs`.

## Project Structure

- `src/`: Contains the FastAPI application code.
- `docker-compose.yml`: Docker Compose configuration file.
- `Dockerfile`: Dockerfile for building the FastAPI application image.

## License

This project is licensed under the MIT License.