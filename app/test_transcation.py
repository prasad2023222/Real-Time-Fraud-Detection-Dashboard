import requests
import random

url = "http://127.0.0.1:8000/predict"

states = ['NC', 'WA', 'ID', 'MT', 'VA', 'PA', 'KS', 'TN', 'IA', 'WV', 'FL',
       'CA', 'NM', 'NJ', 'OK', 'IN', 'MA', 'TX', 'WI', 'MI', 'WY', 'HI',
       'NE', 'OR', 'LA', 'DC', 'KY', 'NY', 'MS', 'UT', 'AL', 'AR', 'MD',
       'GA', 'ME', 'AZ', 'MN', 'OH', 'CO', 'VT', 'MO', 'SC', 'NV', 'IL',
       'NH', 'SD', 'AK', 'ND', 'CT', 'RI', 'DE']

categories = ["gas_transport","grocery_pos","home","shopping_pos","kids_pets","shopping_net","entertainment","food_dining","personal_care","health_fitness","misc_pos","misc_net","grocery_net","travel"]

for i in range(100):

    data = {
        "amt": random.randint(10,400),
        "hour": random.randint(0,23),
        "is_night": random.randint(0,1),
        "date": 6,
        "log_amount": 0,
        "high_amt": random.randint(0,1),
        "user_avg_amt": random.randint(10,100),
        "deviation_amt": random.randint(10,70),
        "spending_ratio": random.uniform(0.5,5),
        "last_1h_trans": random.randint(1,10),
        "gender": random.choice(["M","F"]),
        "distance": random.uniform(1,100),
        "state": random.choice(states),
        "category": random.choice(categories)
    }
    headers = {"x-api-key": "super-secret-key-123"}  # must match .env
    r = requests.post(url,json=data)

   
    print("Transaction:", i+1)
    print("Response:", r.json())
    print("------------------")