def classify_intent(user_input: str) -> str:
    input_lower = user_input.lower()

    # Real-time questions
    if any(kw in input_lower for kw in ["latest", "current", "today", "live rates", "news", "update"]):
        return "real_time_info"

    # Policy comparison
    if any(kw in input_lower for kw in ["compare", "difference", "better plan", "which is best"]):
        return "comparison"

    # Premium or pricing
    if any(kw in input_lower for kw in ["premium", "rate", "cost", "price"]):
        return "premium_info"

    # Family-related needs
    if any(kw in input_lower for kw in ["dependent", "family", "children", "spouse"]):
        return "family_protection"

    # Coverage calculation
    if any(kw in input_lower for kw in ["calculate", "how much coverage", "coverage amount", "need", "sufficient"]):
        return "coverage_calc"

    # Income-based advice
    if any(kw in input_lower for kw in ["income", "salary", "afford", "budget"]):
        return "income_based_advice"

    # Default fallback
    return "general"
