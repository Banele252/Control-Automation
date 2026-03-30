#!/bin/sh

echo "Creating tables..."
python supabase_create_tables.py

echo "Starting server..."
exec "$@"