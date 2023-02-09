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

You may now access the API on your browser via: http://localhost:8080/docs

![image](https://user-images.githubusercontent.com/73839376/216799142-d69cf304-da51-48d7-8e8d-ebb3a19df283.png)

Filter parameters for: **GET /museums-api/v1/artworks/filter**
![image](https://user-images.githubusercontent.com/73839376/216801957-bc35a82c-98f7-4deb-8051-7d3789e3b03b.png)


Successful Response (Example):
![image](https://user-images.githubusercontent.com/73839376/216801921-80236495-9fac-4dbc-a10b-f47c1987da97.png)


