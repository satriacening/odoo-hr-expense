#!/bin/bash

POSTGRES="psql -U $POSTGRES_USER"

# create a shared role to read & write general datasets into postgres
echo "Creating database role: $ODOO_DB_USER"
$POSTGRES <<-EOSQL
CREATE USER $ODOO_DB_USER WITH
    LOGIN
    SUPERUSER
    CREATEDB
    CREATEROLE
    INHERIT
    REPLICATION
    PASSWORD '$ODOO_DB_PASSWORD';
EOSQL
