import psycopg2
import secrets

DB_HOST = secrets.DB_HOST
DB_NAME = secrets.DB_NAME
DB_USER = secrets.DB_USER
DB_PASSWORD = secrets.DB_PASSWORD

def get_connection():
    return psycopg2.connect(
        host=DB_HOST,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
