

import psycopg2
import os
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')

def get_db_connection():
    conn = psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)
    return conn

def create_tables():
    commands = [
        """
        CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
        """,
        """
        CREATE TABLE IF NOT EXISTS Companies (
            company_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
            company_name VARCHAR NOT NULL UNIQUE
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS Categories (
            category_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
            category_name VARCHAR NOT NULL UNIQUE
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS Products (
            product_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
            company_id UUID REFERENCES Companies(company_id) ON DELETE CASCADE,
            company_name VARCHAR NOT NULL,
            price INTEGER,
            description VARCHAR,
            active BOOLEAN DEFAULT true
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS ProductsCategoriesXref (
            product_id UUID REFERENCES Products(product_id) ON DELETE CASCADE,
            category_id UUID REFERENCES Categories(category_id) ON DELETE CASCADE,
            PRIMARY KEY (product_id, category_id)
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS Warranties (
            warranty_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
            product_id UUID UNIQUE REFERENCES Products(product_id) ON DELETE CASCADE,
            warranty_months VARCHAR NOT NULL
        );
        """
    ]

    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        for command in commands:
            cur.execute(command)
        conn.commit()
        cur.close()
        print("Tables created or verified successfully.")
    except Exception as e:
        print(f"Error creating tables: {e}")
    finally:
        if conn is not None:
            conn.close()
