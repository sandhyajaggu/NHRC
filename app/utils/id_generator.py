from app.models.counter import MembershipCounter

PREFIX_MAP = {
    "student": "STU",
    "employee": "EMP",
    "representative": "REP",
    "admin": "ADM"  
}


def generate_membership_id(db, candidate_type):
    counter = db.query(MembershipCounter).filter_by(type=candidate_type).first()

    if not counter:
        counter = MembershipCounter(type=candidate_type, current_value=0)
        db.add(counter)
        db.commit()
        db.refresh(counter)

    counter.current_value += 1
    db.commit()

    return f"NHRC-{PREFIX_MAP[candidate_type]}-{counter.current_value:03}"