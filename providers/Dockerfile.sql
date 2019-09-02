FROM mysql/mysql-server
COPY test.sql  /docker-entrypoint-initdb.d


