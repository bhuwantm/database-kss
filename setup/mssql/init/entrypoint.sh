#!/bin/bash

# Start SQL Server
ACCEPT_EULA=Y /opt/mssql/bin/sqlservr &

# Start the script to create the DB and user
/usr/config/configure-db.sh

# Call extra command
eval $1
