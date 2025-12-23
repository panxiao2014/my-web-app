# my-web-app

For backend: uvicorn main:app --reload --port 8000

For frontend: npm run dev


Docker running:

docker build -f Dockerfile-backend -t my-web-app-backend:latest .

docker build -f Dockerfile-frontend -t my-web-app-frontend:latest .

docker-compose -f docker-compose-oci.yml up

