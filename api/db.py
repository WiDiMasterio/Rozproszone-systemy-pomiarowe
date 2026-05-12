import psycopg2
import tajnyPlik as sec


def get_connection():
    return psycopg2.connect(
        host=sec.DB_HOST,
        dbname=sec.DB_NAME,
        user=sec.DB_USER,
        password=sec.DB_PASSWORD
        )