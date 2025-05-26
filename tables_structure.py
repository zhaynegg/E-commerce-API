import psycopg2
from script2 import mypassword

conn = psycopg2.connect(host="localhost", dbname="e-commerce", user="postgres",
                password=mypassword, port=5432)

cur = conn.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS products (
            id SERIAL PRIMARY KEY,
            product_name VARCHAR(50),
            count INTEGER,
            cost MONEY
            );""")

cur.execute("""CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username VARCHAR(50),
            email VARCHAR(70),
            password VARCHAR(255)
            );""")

cur.execute("""CREATE TABLE IF NOT EXISTS baskets (
            id SERIAL PRIMARY KEY,
            user_id INTEGER,
            product_id INTEGER,
            count INTEGER,
            CONSTRAINT fk_user
                FOREIGN KEY(user_id)
                REFERENCES users(id),
            CONSTRAINT fk_product
                FOREIGN KEY(product_id)
                REFERENCES products(id)
            );""")

conn.commit()

cur.close()
conn.close()