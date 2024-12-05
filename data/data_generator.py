from datetime import datetime, timedelta
import random
import json

# Helper functions to generate random timestamps and plates
def random_plate():
    letters = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=3))
    numbers = ''.join(random.choices('0123456789', k=3))
    return f"{letters}{numbers}"

def random_timestamp(start_date, end_date):
    delta = end_date - start_date
    random_seconds = random.randint(0, int(delta.total_seconds()))
    return (start_date + timedelta(seconds=random_seconds)).timestamp()

# Set date range for the week (28 November to today)
start_date = datetime(2024, 11, 28)
end_date = datetime.now()

# Generate 100 car entries
cars_in = []
cars_out = []
for _ in range(50):  # 50 cars_in entries
    plate = random_plate()
    tickets = [{"plate": plate, "arrival": random_timestamp(start_date, end_date)} for _ in range(random.randint(1, 3))]
    cars_in.append({"plate": plate, "tickets": tickets, "sub": None})

for _ in range(50):  # 50 cars_out entries
    plate = random_plate()
    tickets = [{"plate": plate, "arrival": random_timestamp(start_date, end_date)} for _ in range(random.randint(0, 2))]
    sub = None
    if random.choice([True, False]):
        sub = {
            "plate": plate,
            "length": random.randint(1, 12),
            "start": random_timestamp(start_date, end_date)
        }
    cars_out.append({"plate": plate, "tickets": tickets, "sub": sub})

# Create the database dictionary
database = {
    "cars_in": cars_in,
    "cars_out": cars_out,
    "spaces": 192
}

# Output as JSON
with open("data.json", "w") as outfile:
    json.dump(database, outfile)
