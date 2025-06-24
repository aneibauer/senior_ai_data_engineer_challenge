"""
db/postgres.py

This module provides the asynchronous database connection setup for the application,
using the `databases` library with an asyncpg PostgreSQL backend. It exposes a
`database` instance configured with the application's PostgreSQL connection URL,
which can be imported and used throughout the API for executing asynchronous
database operations.

My PostgreSQL database currently only has one database named `events`
"""
from databases import Database

DATABASE_URL = "postgresql+asyncpg://user:password@postgres:5432/events"

database = Database(DATABASE_URL)