def apply_rules(message: str):
    msg = message.lower()

    if "price" in msg or "cost" in msg:
        return "Please share your requirement. Our team will contact you with pricing."

    if "job" in msg or "career" in msg:
        return "Please send your resume to hr@company.com"

    return None
