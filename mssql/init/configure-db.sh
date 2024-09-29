#!/bin/bash

# wait for MSSQL server to start
export STATUS=0
i=0
while [[ $STATUS -eq 0 ]] || [[ $i -lt 30 ]]; do
	sleep 1
	i=$i+1
	STATUS=$(grep 'Recovery is complete' /var/opt/mssql/log/errorlog* | wc -l)
done

sed -i s/"{DB_NAME}"/"${DB_NAME}"/g /usr/config/setup.sql
sed -i s/"{DB_USERNAME}"/"${DB_USERNAME}"/g /usr/config/setup.sql
sed -i s/"{DB_PASSWORD}"/"${DB_PASSWORD}"/g /usr/config/setup.sql

echo "======= MSSQL SERVER STARTED ========" | tee -a ./status.log

# Run the setup script to create the DB and the schema in the DB
/opt/mssql-tools/bin/sqlcmd -S localhost -U sa -P $MSSQL_SA_PASSWORD -d master -i setup.sql

echo "======= MSSQL CONFIG COMPLETE =======" | tee -a ./status.log
