#!/bin/bash

# Define PostgreSQL connection variables
PG_HOST="localhost"
PG_PORT="5432"
PG_USER="alex"
PG_PASSWORD="xxx"
DB_NAME="short_urls"

# Drop the database
echo "Dropping the database..."
psql -h $PG_HOST -p $PG_PORT -U $PG_USER -d postgres -c "DROP DATABASE IF EXISTS $DB_NAME;"
psql -h $PG_HOST -p $PG_PORT -U $PG_USER -d postgres -c "CREATE DATABASE $DB_NAME;"

echo "Database drop complete."
