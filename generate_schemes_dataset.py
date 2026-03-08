import json
import random

schemes = []

occupations = [
    "farmer",
    "student",
    "daily_worker",
    "unemployed",
    "entrepreneur",
    "all"
]

states = [
    "Uttar Pradesh",
    "Madhya Pradesh",
    "Bihar",
    "Rajasthan",
    "Maharashtra",
    "Gujarat",
    "Punjab",
    "Haryana",
    "Delhi",
    "Karnataka",
    "Tamil Nadu",
    "West Bengal"
]

benefits = [
    "financial assistance",
    "insurance coverage",
    "skill training",
    "housing subsidy",
    "healthcare support",
    "education scholarship",
    "agriculture support",
    "business loan"
]

documents = [
    "Aadhaar Card",
    "Income Certificate",
    "Bank Account",
    "Ration Card",
    "Residence Proof"
]

for i in range(250):

    scheme = {
        "name": f"Government Scheme {i+1}",
        "description": random.choice(benefits) + " provided by the government.",
        "occupation": random.choice(occupations),
        "state": random.choice(states),
        "income_limit": random.randint(100000,500000),
        "benefit": random.choice(benefits),
        "documents": random.sample(documents,3)
    }

    schemes.append(scheme)

with open("schemes_db.json","w") as f:
    json.dump(schemes,f,indent=2)

print("Dataset generated with",len(schemes),"schemes")