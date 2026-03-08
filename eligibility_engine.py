def find_eligible_schemes(profile, schemes):

    results = []

    for s in schemes:

        score = 0

        # income eligibility
        if profile.get("income",0) <= s.get("income_limit",9999999):
            score += 50

        # occupation match
        if s.get("occupation") == "all" or s.get("occupation") == profile.get("occupation"):
            score += 30

        # state bonus
        if s.get("state","all") == "all" or s.get("state") == profile.get("state"):
            score += 20

        s["score"] = score

        results.append(s)

    return results


def rank_schemes(schemes):

    ranked = sorted(
        schemes,
        key=lambda x: x["score"],
        reverse=True
    )

    return ranked[:5]