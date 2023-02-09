# Setup (with Docker Compose)

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

Once the container is running, run migrations

```docker-compose run app alembic revision --autogenerate -m "migration"```

```docker-compose run app alembic upgrade head```

You may access the API documentation on your browser via: http://localhost:8080/docs

![image](https://user-images.githubusercontent.com/73839376/217846431-67358388-e2c8-4b5a-9b54-afb9243d4d38.png)


