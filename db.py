import os
import psycopg2
from contextlib import contextmanager
from dotenv import load_dotenv

load_dotenv()  

DB_CONFIG = {
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST"),
    "port": int(os.getenv("DB_PORT", 5432)),
}

@contextmanager
def get_connection():
    conn = psycopg2.connect(**DB_CONFIG)
    try:
        yield conn
    finally:
        conn.close()

def get_next_run_id():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT nextval('scrape_run_id_seq')")
            run_id = cur.fetchone()[0]
            return run_id

def insert_titles(table_name, titles, run_id):
    """
    Insert scraped data into the specified table.
    Each title tuple must contain:
    (title, brand_or_model, product_link, photo_url, price_amount, price_currency, price_tax_text)
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            for (
                title, brand_or_model, product_link, photo_url,
                price_amount, price_currency, price_tax_text
            ) in titles:
                cur.execute(
                    f"""
                    INSERT INTO {table_name} 
                    (title, run_id, brand_or_model, product_link, photo_url, price_amount, price_currency, price_tax_text)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                    (
                        title, run_id, brand_or_model, product_link, photo_url,
                        price_amount, price_currency, price_tax_text
                    )
                )
        conn.commit()

def get_latest_generators(table_name):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(f"""
                SELECT * FROM {table_name}
                WHERE run_id = (
                    SELECT MAX(run_id) FROM {table_name}
                )
                ORDER BY id
            """)
            rows = cur.fetchall()
            return rows

def get_latest_scraped_at(table_name):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(f"""
                SELECT scraped_at FROM {table_name}
                WHERE run_id = (SELECT MAX(run_id) FROM {table_name})
                ORDER BY scraped_at DESC
                LIMIT 1
            """)
            row = cur.fetchone()
            return row[0] if row else None
