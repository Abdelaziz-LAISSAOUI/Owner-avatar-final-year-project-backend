from sqlalchemy.orm import Session
from ..utilities import verify_password ,get_password_hash
from ..schemas import admin_schemas
from ..models import Admin

def get_admin(db: Session, username: str):
    return db.query(Admin).filter(Admin.username == username).first()

def create_admin(db: Session, admin: admin_schemas.AdminCreate):
    admin.password = get_password_hash(admin.password)
    db_admin = Admin(**admin.model_dump())
    db.add(db_admin)
    db.commit()
    db.refresh(db_admin)
    db_admin.password = None
    return db_admin

def authenticate_admin(db: Session, username: str, password: str):
    admin = get_admin(db, username)
    if not admin:
        return False
    if not verify_password(password, admin.password):
        return False
    return admin