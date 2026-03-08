import re

def parse_voice_profile(text):

    profile = {}

    text = text.lower()

    # occupation
    if "किसान" in text or "farmer" in text:
        profile["occupation"] = "farmer"

    if "मजदूर" in text or "labour" in text:
        profile["occupation"] = "daily_worker"

    if "student" in text or "विद्यार्थी" in text:
        profile["occupation"] = "student"

    if "बेरोजगार" in text or "unemployed" in text:
        profile["occupation"] = "unemployed"

    # state detection
    states = [
        "uttar pradesh","madhya pradesh","bihar",
        "rajasthan","maharashtra","gujarat",
        "punjab","haryana","delhi",
        "karnataka","tamil nadu","west bengal"
    ]

    for s in states:
        if s in text:
            profile["state"] = s.title()

    # lakh detection
    lakh = re.search(r'(\d+)\s*लाख', text)
    if lakh:
        profile["income"] = int(lakh.group(1)) * 100000

    # crore detection
    crore = re.search(r'(\d+)\s*करोड़', text)
    if crore:
        profile["income"] = int(crore.group(1)) * 10000000

    # plain number detection
    number = re.search(r'(\d+)', text)
    if number and "income" not in profile:
        profile["income"] = int(number.group(1))

    return profile