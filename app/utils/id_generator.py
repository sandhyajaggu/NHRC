from app.models.counter import MembershipCounter
from app.models.member import Member

PREFIX_MAP = {
    "student": "STU",
    "employee": "EMP",
    "representative": "REP",
    "admin": "ADM"
}


def generate_membership_id(db, candidate_type):
    prefix = PREFIX_MAP[candidate_type]

    counter = db.query(MembershipCounter).filter_by(type=candidate_type).first()

    if not counter:
        counter = MembershipCounter(type=candidate_type, current_value=0)
        db.add(counter)
        db.commit()
        db.refresh(counter)

    while True:
        counter.current_value += 1

        membership_id = f"NHRC-{prefix}-{counter.current_value:03}"

        # 🔥 check if already exists
        exists = db.query(Member).filter_by(membership_id=membership_id).first()

        if not exists:
            break

    db.commit()

    return membership_id