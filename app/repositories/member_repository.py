from sqlalchemy.orm import Session
from app.models.member import Member

class MemberRepository:
    @staticmethod
    def create(db: Session, payload: dict):
        member = Member(**payload)
        db.add(member)
        db.commit()
        db.refresh(member)  
        return member

    @staticmethod
    def get_by_id(db: Session, member_id: int):
        return db.query(Member).filter(Member.id == member_id).first()