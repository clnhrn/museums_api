# Museums API

The Museums API contains artists and artworks data from 1950 to 2021 on 130 museums all around the U.S. 

## Setup for Testing

### Install Docker

If you don't have Docker installed yet, check the links below to install it on your system

#### For Windows
https://docs.docker.com/desktop/install/windows-install/
#### For Mac
https://docs.docker.com/desktop/install/mac-install/
#### For Linux
https://docs.docker.com/desktop/install/linux-install/

### Create env file

Create a .env file. For testing, we're creating a pgadmin and postgresql_db container so we need to include the following environment variables:

``` .env
DATABASE_URL=postgresql://cln:museum_pass@db:5432/records
DB_USER=cln
DB_PASSWORD=museum_pass
DB_NAME=records
PGADMIN_EMAIL=admin@admin.com
PGADMIN_PASSWORD=admin
```

In production, we might need to add more environment variables depending on the database hosting service provider (i.e. Google Cloud) and remove the pgadmin variables since we only need to establish a connection to the PostgreSQL database.

### Run Docker Compose
To start building the containers needed to run the application, enter the command below:

```bash
docker-compose up
```
### Restore SQL Dump

Check the volumes of the database container to see where you can save your dump file. To do this, you need to get the container ID of the database. Run the command below to get the list of running containers and their details.

```bash
docker ps
```

Get the container ID of postgresql_db and enter the command below to see the available volumes

```bash
docker inspect -f '{{ json .Mounts }}' <container ID> | python -m json.tool
```

In my case, the command returned 1 volume that has a "Destination" path (/var/lib/postgresql/data). This is where we will store the dump file.

To copy the dump file from your local machine to the Docker container, use the docker cp command with the following format:

```bash
docker cp <path to dump file in host machine> <container name>:<path to volume where dump file will be saved>
```

For example:

```bash 
docker cp /path/to/records.sql postgresql_db:/var/lib/postgresql/data/records.sql
```

Before restoring the dump, we need to delete the existing schema. Run the command below to connect to the database via psql

```
psql postgresql://cln:museum_pass@localhost:6543/records
```

Once connected to the 'records' database, enter the SQL statement below to delete the existing schema

``` sql
DROP SCHEMA public CASCADE;
```

Finally, restore the dump in the docker container using pg_restore

```bash
docker exec postgresql_db pg_restore -U cln -d records /var/lib/postgresql/data/records.sql
```

Query the data via psql (or log in to pgadmin if you prefer a GUI) to check if the restoration was successful. Now, we can test the API!

## Using the API

You may access the API docs via http://localhost:8080/docs

Before anything else, you need to register using the "Register" endpoint. Send a POST request and provide a username and password.

```bash
curl -X 'POST' \
  'http://localhost:8080/museums-api/register' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "username": "user",
  "password": "museum_trial"
}'
```

After registration, you can login via the "Login" endpoint. Send a POST request and provide the username and password that you used to register. The response includes a token that you will need in order to send authenticated requests to the API.

```bash
curl -X 'POST' \
  'http://localhost:8080/museums-api/login' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "username": "user",
  "password": "museum_trial"
}'
```
Here's a sample response:
```bash
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2Nzc3NDM5MzMsImlhdCI6MTY3NzY1NzUzMywic3ViIjoiY2VsaW5lIn0.laZxHqVHC0v-F60z6SyE-K7jnh4SkQVidl3bRv1bIpA"
}
```

Now, you can include the token in your headers when sending a GET request to the API.

```bash
curl -X 'GET' \
  'http://localhost:8080/museums-api/artists?page=1&size=50' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2Nzc3NDM5MzMsImlhdCI6MTY3NzY1NzUzMywic3ViIjoiY2VsaW5lIn0.laZxHqVHC0v-F60z6SyE-K7jnh4SkQVidl3bRv1bIpA'
```

In the example above, we're sending a GET request to the "Get All Artists" endpoint with the default parameters (page=1 and size=50). We also included the provided token as our Authorization header to authenticate the request.

You're all set! Feel free to test out all the endpoints and let me know if you encounter any errors.

*Note that a token is only valid for 24 hours. To get a new token, you need to login again.*
