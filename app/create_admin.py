from app.core.database import SessionLocal

from app.models.member import Member

from app.core.security import hash_password


def create_admin():

    db = SessionLocal()

    existing = db.query(Member).filter(
        Member.email == "shivakrishna@nhrc.com"
    ).first()

    if existing:

        print("Admin already exists")

        # OPTIONAL:
        # update role if wrong

        existing.role = "ADMIN"

        db.commit()

        print("Admin role updated to ADMIN")

        return

    admin = Member(

        membership_id="ADMIN001",

        full_name="Shiva Krishna",

        email="shivakrishna@nhrc.com",

        password_hash=hash_password("Shiva@123"),

        role="ADMIN",

        candidate_type="admin",

        status="approved"
    )

    db.add(admin)

    db.commit()

    print("Admin created successfully")


if __name__ == "__main__":
    create_admin()