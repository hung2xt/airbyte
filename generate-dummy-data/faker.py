import psycopg2
from faker import Faker
import itertools

# Database connection parameters
db_params = {
    "dbname": "sandbox-img",
    "user": "cat02",
    "password": "asd@1234",
    "host": "172.17.0.2",
    "port": 5432
}

# Function to generate fake data
def generate_data(num_records):
    fake = Faker()
    for _ in range(num_records):
        yield (fake.uuid4(), fake.name(), fake.email(), fake.city(), fake.company(), fake.country())

# Function to insert data in batches
def batch_insert(cursor, data, batch_size=1000):
    query = "INSERT INTO dummy_data_dev (user_id, name, email, city, company, country) VALUES (%s, %s, %s, %s, %s, %s)"
    batch = []
    for record in data:
        batch.append(record)
        if len(batch) >= batch_size:
            cursor.executemany(query, batch)
            batch = []
    if batch:
        cursor.executemany(query, batch)

# Main function to insert 30 million records
def main():
    try:
        connection = psycopg2.connect(**db_params)
        cursor = connection.cursor()
        batch_insert(cursor, generate_data(10000000))
        connection.commit()
        print("Data inserted successfully")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if connection:
            cursor.close()
            connection.close()

if __name__ == "__main__":
    main()
