from core.database import SessionLocal, Base, engine
from models.user import User, RoleEnum
from core.security import get_password_hash

def init_db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    
    # Check if admin already exists
    admin = db.query(User).filter(User.email == "admin@finance.com").first()
    if not admin:
        admin_user = User(
            name="Admin User",
            email="admin@finance.com",
            hashed_password=get_password_hash("adminpassword"),
            role=RoleEnum.Admin
        )
        db.add(admin_user)
        db.commit()
        print("Created initial admin: admin@finance.com / adminpassword")
    else:
        print("Admin user already exists.")
    
    db.close()

if __name__ == "__main__":
    init_db()
