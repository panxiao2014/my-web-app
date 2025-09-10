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

# How to run

Frontend:

```sh
cd frontend

npm run dev
```

Backend:
```sh
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
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
docker run --name backend --network myapp-network -p  my-backend
docker run --name frontend --network myapp-network -p 3000:80 my-frontend
```
Visit http://localhost:3000/ to verify.