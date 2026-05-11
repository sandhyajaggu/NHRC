from app.db.base_class import SessionLocal
from app.models.member import Member
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_admin():
    db = SessionLocal()

    existing = db.query(Member).filter(Member.email == "admin@nhrc.com").first()
    if existing:
        print(" Admin already exists")
        return



    admin = Member(
        membership_id="ADMIN001",
        full_name="Shiva Krishna",
        email="shivakrishna@nhrc.com",
        password_hash=pwd_context.hash("Shiva@123"),
        candidate_type="admin",
        role="admin"
    )

    db.add(admin)
    db.commit()
    db.close()

    print(" Admin created successfully")

if __name__ == "__main__":
    create_admin()