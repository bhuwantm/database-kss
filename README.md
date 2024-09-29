# Data Lake Setup In Docker
Create a docker container for datalake database.


## Setup

### Create Environment Variables
```bash
cp .env.example .env
```

### Update Data Lake Database Credentials in .env as required
```
MSSQL_SA_PASSWORD=<MSSQL_SA_PASSWORD>
DB_USERNAME=<DB_USERNAME>
DB_PASSWORD=<DB_PASSWORD>
DB_NAME=<DB_NAME>
```

### Container up
```bash
docker-compose up -d
```
