## 🏁 Getting Started

### Prerequisites

Make sure you have **Docker** and **Docker Compose** installed on your machine.

### Installation & Running

1.  **Clone the repository:**
    ```bash
    git clone <your-repo-url>
    cd Spy-Cat-Agency
    ```

2.  **Build and Start Containers:**
    ```bash
    docker-compose up --build
    ```

3.  **Apply Migrations:**
    (Crucial step to create database tables)
    ```bash
    docker-compose run --rm web python manage.py migrate
    ```

The API should now be running at `http://127.0.0.1:8000/`.

---

## 📖 Documentation (Swagger UI)

Interactive API documentation is available at:

👉 **[http://127.0.0.1:8000/api/docs/](http://127.0.0.1:8000/api/docs/)**

You can test all endpoints directly from the browser.

---

## 🧪 Testing

The project uses `pytest` for comprehensive testing (Models, API endpoints, Signals, Validations).

To run all tests:

```bash
docker-compose run --rm web pytest
