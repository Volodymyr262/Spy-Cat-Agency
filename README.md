## 🏁 Getting Started

### Prerequisites

Make sure you have **Docker** and **Docker Compose** installed on your machine.

### Installation & Running

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/Volodymyr262/Spy-Cat-Agency
    cd Spy-Cat-Agency
    ```

2.  **Build and Start Containers:**
    ```bash
    docker-compose up --build
    ```

3.  **Apply Migrations:**
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

```

## POSTMAN collection
**https://bold-meadow-956093.postman.co/workspace/workspace1~953431f8-961b-4aa2-ba6e-11655c17fbe5/collection/24779787-e27cbccc-6baa-4ab4-ad10-dc886a6d8fc3?action=share&creator=24779787**


