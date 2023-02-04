# Setup

Create .env file and include the following variables (input your credentials)

``` 
DATABASE_URL=postgresql://user:password@db:5432/records_db
DB_USER=user
DB_PASSWORD=password
DB_NAME=records_db 
PGADMIN_EMAIL=admin@admin.com
PGADMIN_PASSWORD=admin
```


Run Docker Compose

```docker-compose up```

Once the container is running, run migrations using alembic

```docker-compose run app alembic revision --autogenerate -m "migration"```

```docker-compose run app alembic upgrade head```

You may now access the API on your browser via: http://localhost:8000/docs

