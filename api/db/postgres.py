# db/postgres.py
import psycopg2
from databases import Database

# def get_connection():
#     return psycopg2.connect(
#         host="postgres",
#         database="events",
#         user="user",
#         password="password"
#     )

DATABASE_URL = "postgresql+asyncpg://user:password@postgres:5432/events"

database = Database(DATABASE_URL)