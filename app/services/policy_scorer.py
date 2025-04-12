def score_policy(policy: dict, user_profile: dict) -> int:
    score = 0

    # Income-based affordability
    income = user_profile.get("income")
    premium = policy.get("monthly_premium")
    if income and premium:
        if premium <= income * 0.05:
            score += 2
        elif premium <= income * 0.1:
            score += 1
        else:
            score -= 1

    # Family coverage relevance
    if user_profile.get("family_size", 0) > 0:
        if policy.get("has_family_coverage"):
            score += 2

    # Match financial goals with policy type
    goal = user_profile.get("financial_goal")
    ptype = policy.get("type")  # term, whole, universal, etc.
    if goal and ptype:
        if goal == "long_term" and ptype == "whole":
            score += 2
        elif goal == "short_term" and ptype == "term":
            score += 2

    # Rider features
    if policy.get("includes_riders"):
        score += 1

    # Optional: User-specific preferences (e.g. critical illness, disability)
    preferred_riders = user_profile.get("preferred_riders", [])
    policy_riders = policy.get("riders", [])
    if preferred_riders and policy_riders:
        matched = set(preferred_riders).intersection(set(policy_riders))
        score += len(matched)

    return score


def rank_policies(policies: list, user_profile: dict) -> list:
    """
    Returns a list of tuples (policy, score), sorted by score descending
    """
    scored = [(policy, score_policy(policy, user_profile)) for policy in policies]
    return sorted(scored, key=lambda x: x[1], reverse=True)
