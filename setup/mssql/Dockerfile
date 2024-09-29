FROM mcr.microsoft.com/mssql/server:2017-latest

RUN mkdir -p /usr/config
WORKDIR /usr/config

COPY ./init/configure-db.sh /usr/config/configure-db.sh
COPY ./init/entrypoint.sh /usr/config/entrypoint.sh
COPY ./init/setup.sql.template /usr/config/setup.sql

RUN chmod +x /usr/config/entrypoint.sh
RUN chmod +x /usr/config/configure-db.sh

ENV PATH="$PATH:/opt/mssql-tools/bin"

ENTRYPOINT ["./entrypoint.sh"]

CMD ["tail -f /var/opt/mssql/log/errorlog*"]

HEALTHCHECK --interval=15s CMD grep -q "MSSQL CONFIG COMPLETE" /usr/config/status.log
