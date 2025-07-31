import random
from datetime import date, timedelta
from faker import Faker
# from core.database import get_database


from pymongo import MongoClient
import os

MONGODB_URL = "mongodb://mongo:27017/"
MONGODB_DB_NAME ="patient_management"

client = MongoClient(MONGODB_URL)
db = client[MONGODB_DB_NAME]

def get_database():
    return db


fake = Faker()
genders = ["male", "female", "other"]

def random_date(start_year=1950, end_year=2015):
    start_date = date(start_year, 1, 1)
    end_date = date(end_year, 12, 31)
    delta = end_date - start_date
    return str(start_date + timedelta(days=random.randint(0, delta.days)))

def generate_sample_patients(n=100):
    patients = []
    for _ in range(n):
        gender = random.choice(genders)
        first_name = fake.first_name_male() if gender == "male" else fake.first_name_female() if gender == "female" else fake.first_name()
        last_name = fake.last_name()
        email = fake.unique.email()
        phone = fake.msisdn()[:15]
        dob = random_date()
        patients.append({
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "phone": phone,
            "gender": gender,
            "dob": dob
        })
    return patients

def insert_sample_patients():
    db = get_database()
    patients = generate_sample_patients(100)
    db["patients"].insert_many(patients)
    print(f"Inserted {len(patients)} sample patients.")

if __name__ == "__main__":
    insert_sample_patients() 