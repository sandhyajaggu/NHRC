from app.models.counter import MembershipCounter

PREFIX_MAP = {
    "student": "STU",
    "employee": "EMP",
    "representative": "REP",
    "admin": "ADM"
}


def generate_membership_id(db, candidate_type: str):
    #  Normalize input
    candidate_type = candidate_type.strip().lower()

    #  Validate candidate_type
    if candidate_type not in PREFIX_MAP:
        raise ValueError(f"Invalid candidate_type: {candidate_type}")

    #  Fetch counter safely (case-insensitive)
    counter = (
        db.query(MembershipCounter)
        .filter(MembershipCounter.type.ilike(candidate_type))
        .first()
    )

    #  Create if not exists
    if not counter:
        counter = MembershipCounter(type=candidate_type, current_value=0)
        db.add(counter)
        db.commit()
        db.refresh(counter)

    #  Increment safely
    counter.current_value += 1
    db.commit()
    db.refresh(counter)

    #  Generate ID
    prefix = PREFIX_MAP[candidate_type]
    return f"NHRC-{prefix}-{counter.current_value:03}"