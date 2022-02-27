import psycopg
from faker import Faker
import os
from dotenv import load_dotenv


load_dotenv()


fake = Faker()
fake.seed_instance(17)


def create_new_database_with_index():
    with psycopg.connect(
        dbname=os.getenv("DATABASE_DBNAME"),
        user=os.getenv("DATABASE_USERNAME"),
        password=os.getenv("DATABASE_PASSWORD"),
        host="localhost",
        port=5432
    ) as conn:
        with conn.cursor() as cur:
            cur.execute("CREATE EXTENSION IF NOT EXISTS pg_trgm")
            cur.execute("DROP TABLE IF EXISTS domainindexed")
            cur.execute("""
                CREATE TABLE domainindexed (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(60))
                """)
            cur.execute("""
                CREATE INDEX trgm_idx2 ON domainindexed USING GIN(name gin_trgm_ops)""")
            for i in range(3000):
                if i % 30 == 0:
                    print(i)
                label = fake.domain_word().lower()
                tup = []
                for j in range(1500):
                    name = label + "=" + fake.url().lower()
                    tup.append(name)
                args_str = ','.join("('" + x + "')" for x in tup)
                cur.execute("INSERT INTO domainindexed (name) VALUES " + args_str)
            conn.commit()
    print("Database setup finished")


if __name__ == "__main__":
    create_new_database_with_index()

