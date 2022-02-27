import psycopg
from faker import Faker
import os
from dotenv import load_dotenv


load_dotenv()


fake = Faker()
fake.seed_instance(17)


def create_new_database():
    with psycopg.connect(
        dbname=os.getenv("DATABASE_DBNAME"),
        user=os.getenv("DATABASE_USERNAME"),
        password=os.getenv("DATABASE_PASSWORD"),
        host="localhost",
        port=5432
    ) as conn:
        with conn.cursor() as cur:
            cur.execute("DROP TABLE IF EXISTS domain")
            cur.execute("""
                CREATE TABLE domain (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(60))
                """)
            for i in range(3000):
                if i % 30 == 0:
                    print(i)
                label = fake.domain_word().lower()
                tup = []
                for j in range(1500):
                    name = label + "=" + fake.url().lower()
                    tup.append(name)
                args_str = ','.join("('" + x + "')" for x in tup)
                cur.execute("INSERT INTO domain (name) VALUES " + args_str)
            conn.commit()
    print("Database setup finished")


if __name__ == "__main__":
    create_new_database()

