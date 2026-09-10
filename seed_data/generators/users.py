import uuid
import random
from datetime import datetime, timezone
from faker import Faker
from seed_data.config import supabase

fake = Faker("es_CO")

# Namespace for uuid
NAMESPACE = uuid.UUID("a1b2c3d4-e5f6-7890-abcd-ef1234567890")


# availables roles base on db schema
GENDERS = ["Female", "Male", "Other"]
ROLES = ["User", "Admin"]
CURRENCIES = ["COP","USD","EUR","GBP","MXN"]

NUM_USERS = 500

def _dirty_email(real_email: str) -> str:
    """ Returns an invalid email to simulate dirt data"""
    options = [
        real_email.replace("@", ""), # Space instead of @
        real_email.split("@")[0],   # Without domain
        "@" + real_email.split("@")[1] # Without user
    ]

    return random.choice(options)


def _dirty_date() -> str:
    """Returns a date with an incorrect format"""
    options = [
        "31-02-2023",
        "2024/13/45",
        "not-a-date",
        "00-00-0000"
    ]

    return random.choice(options)

def seed_users() -> list[dict]:
    """
    Generates NUM_USERS users with almost all data clean, but with ~10% invalid eails, ~5% invalid dates, ~20% optional columns nulls and ~5% soft-deleted
    """

    print(f"Generando {NUM_USERS} usuarios...")
    users = []
    for i in range(NUM_USERS):
        user_id = str(uuid.uuid5(NAMESPACE, f"user.{i}"))

        # birth_date: 5% invalid format
        if random.random() < 0.05:
            birth_date = _dirty_date()
        else:
            birth_date = str(fake.date_of_birth(mininum_age=18, maximum_age=70))


        # Email: 10% invalid
        real_email = fake.email()
        email = _dirty_email(real_email) if random.random() < 0.1 else real_email

        # soft-delete: 5% deleted users
        deleted_at = (
            str(fake.date_time_between(start_date="-6m", end_date="now",tzinfo=timezone.utc))
            if random.random() < 0.05
            else None
        )

        user = {
            "id": user_id,
            "document_id": fake.numerify("##########"),
            "name": fake.name(),
            "email": email,
            "birth_date": birth_date,

            # optional columns: 20% null data
            "address": fake.address() if random.random() < 0.20 else None,
            "phone": fake.phone_number if random.random() < 0.2 else None,
            "gender": random.choice(GENDERS) if random.random() < .2 else None,
            "role": "Admin" if i < 5 else "User", # First 5 users are admin
            "preferred_currency_code": random.choice(CURRENCIES),
            "two_factor_enabled": random.choice([True, False]),
            "created_at": str(fake.date_time_between(start_date="-2y",end_date="now",tzinfo=timezone.utc)),
            "updated_at": str(datetime.now(timezone.utc)),
            "deleted_at": deleted_at
        }

        users.append(user)

    # Insert lots of 100 records
    inserted = []
    for i in range(0, len(users), 100):
        batch = users[i : i + 100]
        response = supabase.table("users").upsert(batch, on_conflict="id").execute()
        inserted.extend(response.data)
        print(f" Lote {i // 100 + 1}: {len(response.data)} usuarios")

    print(f"{len(inserted)} usuarios insertados.")
    return inserted