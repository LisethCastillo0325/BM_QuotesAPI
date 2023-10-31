#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username $POSTGRES_USER <<-EOSQL
    DROP DATABASE IF EXISTS ms_quotes_db;
    DROP ROLE IF EXISTS ms_quotes;

    CREATE USER ms_quotes;
    CREATE DATABASE ms_quotes;
    GRANT ALL PRIVILEGES ON DATABASE ms_quotes TO ms_quotes;

    ALTER USER ms_quotes WITH PASSWORD 'ms_quotes';
EOSQL

pg_restore -U ms_quotes -d ms_quotes -c -v ./ms_quotes_sql