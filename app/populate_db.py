import random
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import User, Request

NUM_ADMINS = 2
NUM_MANAGERS = 5
NUM_USERS_PER_MANAGER = 100
NUM_REQUESTS_PER_USER = 5

def populate_database():
    db: Session = SessionLocal()

    try:
        db.query(Request).delete()
        db.query(User).delete()
        db.commit()

        for i in range(NUM_ADMINS):
            admin = User(
                username=f"admin{i + 1}",
                hashed_password="adminpasswordnotsecure",
                role="admin"
            )
            db.add(admin)

        db.commit()

        for i in range(NUM_MANAGERS):
            manager = User(
                username=f"manager{i + 1}",
                hashed_password="managerpasswordnotsecure",
                role="manager"
            )
            db.add(manager)
            db.commit()

            for j in range(NUM_USERS_PER_MANAGER):
                user = User(
                    username=f"user_{i + 1}_{j + 1}",
                    hashed_password="userpasswordnotsecure",
                    role="user",
                    manager_id=manager.id
                )
                db.add(user)
                db.commit()

                for k in range(NUM_REQUESTS_PER_USER):
                    request = Request(
                        bottoken="test_bot_token",
                        chatid=f"{random.randint(100000, 999999)}",
                        message=f"Test message {k + 1} from user_{i + 1}_{j + 1}",
                        response="Test response",
                        user_id=user.id
                    )
                    db.add(request)

        db.commit()
        print("Database populated successfully!")

    except Exception as e:
        db.rollback()
        print(f"Error populating database: {e}")

    finally:
        db.close()


if __name__ == "__main__":
    populate_database()
