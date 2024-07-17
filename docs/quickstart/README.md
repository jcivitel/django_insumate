# Quickstart with docker-compose

## Prerequisites
- Docker and Docker Compose installed on your system

## Steps

1. Save the provided `docker-compose.yml` file in your project directory.

2. **Important**: Change the environment variables
   Before proceeding, modify the following environment variables in the `docker-compose.yml` file:
   - `MAIN_DATABASE_USER`
   - `MAIN_DATABASE_PASSWD`
   - `MARIADB_USER`
   - `MARIADB_PASSWORD`
   - `MARIADB_ROOT_PASSWORD`

   These values are publicly known and must be changed for security reasons.

3. Open a terminal and navigate to the directory containing the `docker-compose.yml` file.

4. Run the following command to start the services:
  `docker-compose up -d`
5. The Insumate application will be available at `http://localhost:8000`.

6. To stop the services, run: `docker-compose down`

## Additional Notes
- The MariaDB data is persisted in the `./mysql` directory.
- The Insumate service depends on both MariaDB and Redis services being healthy/started.
