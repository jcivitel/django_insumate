# Quickstart with docker-compose

## Prerequisites
- Docker and Docker Compose installed on your system

## Steps

1. Save the provided [docker-compose.yml](docker-compose.yml) and [nginx](nginx.conf) file in your project directory.

2. **Important**: Change the environment variables
   Before proceeding, modify the following environment variables in the `docker-compose.yml` file:
   - `MAIN_DATABASE_USER`
   - `MAIN_DATABASE_PASSWD`
   - `MARIADB_USER`
   - `MARIADB_PASSWORD`
   - `MARIADB_ROOT_PASSWORD`
   - `REGISTRATION_ENABLED`        -> by default is this set to `True`, but if you don't want any user to register set this to `False`

> [!IMPORTANT]
>
> if you want to use this installation publicly, you should use `DEBUG=False` and TLS certificates. In order to use certificates, you must choose a domain name.
>
> - `CORS_ALLOWED_ORIGINS`     //Needs to be your domain like `https://insumate.example.com`
> - `CSRF_TRUSTED_ORIGINS`     //Needs to be your domain like `https://insumate.example.com`
><br><br>
> Here is a guide on how to create certificates with [Let's Encrypt](https://letsencrypt.org/getting-started).

   These values are publicly known and must be changed for security reasons.

3. Open a terminal and navigate to the directory containing the `docker-compose.yml` file.

4. Run the following command to start the services:
  `docker-compose up -d`
5. The Insumate application will be available at `http://<ip-of-your-docker>`.

6. To stop the services, run: `docker-compose down`

>  [!NOTE]
> - The MariaDB data is persisted in the `./mysql` directory.
> - The Insumate service depends on both MariaDB and Redis services being healthy/started.
