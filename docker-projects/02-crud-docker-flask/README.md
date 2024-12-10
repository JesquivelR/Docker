# CRUD Application with Flask and Docker 🐳

This project demonstrates how to build a simple **CRUD web application** using **Flask** as the web framework and **PostgreSQL** as the database. Docker is used to containerize the application, making it portable and easy to deploy.

---

## 📝 Project Overview

The purpose of this project is to:
- Understand how to create a RESTful API using Flask.
- Learn how to connect Flask with a PostgreSQL database.
- Use Docker and Docker Compose for efficient application deployment.

---

## 🚀 Getting Started

Follow these steps to set up and run the project on your local machine.

### Prerequisites
- Docker and Docker Compose installed. [Get Docker here](https://www.docker.com/).
- Basic knowledge of Python, Docker, Postgres, and REST APIs.

### Steps to Run

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/JesquivelR/Docker.git
   cd docker-projects/02-crud-docker-flask
   ```
2. **Run the Project with Docker Compose:**
    ```bash
    docker-compose build
    docker-compose up
    ```
3. **Access the Application:**
Open your browser and navigate to: `http://localhost:4000`

4. **Stop the Application:**
    ```bash
    docker-compose down
    ```
---

## 📂 Project Structure

    02-crud-docker-flask/
    ├── app.py               # Main Flask application file
    ├── diagrams/            # Diagrams directory
    ├── docker-compose.yml   # Docker Compose configuration
    ├── Dockerfile           # Docker image setup
    └── requirements.txt     # Python dependencies

---

## 🌟 Features
- **CRUD Operations:** Manage entities like Owners and Vehicles.
- **PostgreSQL Integration:** Reliable and efficient database.
- **RESTful API:** Simplified communication with endpoints.
- **Dockerized Environment:** Easy to run and deploy.

---

## 🔧 API Endpoints
### Endpoints
- **Owners** (`/owners`)
    - **POST** `/owners`: Add a new owner.
    - **GET** `/owners/<id>`: Retrieve an owner's details.

- **Vehicles** (`/vehicles`)
    - **POST** `/vehicles`: Add a new vehicle.
    - **GET** `/vehicles`: List all vehicles.
    - **PUT** `/vehicles/<id>`: Update a vehicle's details.
    - **DELETE** `/vehicles/<id>`: Delete a vehicle.

### Interact with the API using `curl`

1. **Create an Owner**

    To create a new **Owner**, you can send a `POST` request with the data in JSON format:

    ```bash
    curl -X POST http://localhost:4000/owners \
    -H "Content-Type: application/json" \
    -d '{
    "name": "Jorge Esquivel",
    "email": "jesquivelr@example.com"
    }'
    ```

2. **Create a Vehicle**

    To add a Vehicle associated with an existing Owner, use the following `POST` command:

    ```bash
    curl -X POST http://localhost:4000/vehicles \
    -H "Content-Type: application/json" \
    -d '{
    "brand": "Toyota",
    "model": "Corolla",
    "year": 2020,
    "specifications": {"color": "red", "engine": "hybrid"},
    "owner_id": 1
    }'
    ```

3. **View Existing Vehicles**

    To retrieve all Vehicles registered, execute:

    ```bash
    curl -X GET http://localhost:4000/vehicles
    ```

4. **Update a Vehicle**

    If you need to update the details of a specific Vehicle, use the following `PUT` command:

    ```bash
    curl -X PUT http://localhost:4000/vehicles/1 \
    -H "Content-Type: application/json" \
    -d '{
    "brand": "Honda",
    "model": "Civic",
    "year": 2022,
    "specifications": {"color": "blue", "engine": "petrol"}
    }'
    ```

5. **Delete a Vehicle**

    To delete a Vehicle from the database, run a `DELETE` request:

    ```bash
    curl -X DELETE http://localhost:4000/vehicles/1
    ```

---

## 📊 Database Diagram (ERD)

![img](./diagrams/Entity%20Relationship%20Diagram.jpg)

### Diagram Explanation:
1. **Owner Table**:
    - Fields: `id`, `name`, `email`.
    - A single owner can have multiple vehicles.

2. **Vehicle Table**:
    - Fields: `id`, `brand`, `model`, `year`, `specifications`, `owner_id`.
    - Each vehicle belongs to one owner.

---

## 🛠 How to Customize

- Update the `app.py` file to modify application logic.
- Edit `docker-compose.yml` to configure additional services.
- Restart the project to apply changes:

    ```bash
    docker-compose down
    docker-compose up --build
    ```

---

## 🤝 Contributing
Contributions are welcome! Feel free to:
- Open issues for bugs or feature requests.
- Submit pull requests with improvements or additional features.

---

## Author
**Jorge Esquivel**  
Find more of my projects on [GitHub](https://github.com/JesquivelR).