# Setup
```sh
cd my-web-app
python -m venv .venv
.venv\Scripts\activate
cd frontend
npm install
cd ../backend
pip install -r requirements.txt
```

# Update database schema:
```
sqlacodegen postgresql://<username>:<password>@localhost:5432/userdb --outfile backend/app/users/models.py
```

# How to run

Backend:
```sh
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Frontend:

```sh
cd frontend

npm run dev
```

# Run in docker
Build images:
```
docker build -f Dockerfile-frontend -t my-frontend:latest .
docker build -f Dockerfile-backend -t my-backend:latest .
```
Create newtork:
```
docker network create myapp-network
```
Start backend and frontend:
```
export POSTGRES_PASSWORD=<your postgres password>
docker-compose up
```
Visit http://localhost:5173/ to verify.