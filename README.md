# Setup

Run Docker Compose

docker-compose up

Once the container is running, run migrations using alembic

docker-compose run app alembic revision --autogenerate -m "New Migration"
docker-compose run app alembic upgrade head

You may now access the API on your browser.

