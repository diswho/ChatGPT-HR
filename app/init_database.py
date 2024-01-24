from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import Base, get_database_local, get_engine_local, SessionLocal, User, Role, RoleUser,pwd_context


def init() -> None:
    # Create the engine
    # engine = create_engine(get_database_local)
    # Base.metadata.create_all(bind=engine)
    # Session = sessionmaker(bind=engine)
    # session = Session()
    # Session = sessionmaker(bind=get_engine_local)
    try:
        Base.metadata.create_all(bind=get_engine_local)
        session = SessionLocal()

        role_user = Role(name="user")
        role_moderator = Role(name="moderator")
        role_admin = Role(name="admin")

        session.add_all([role_user, role_moderator, role_admin])
        session.commit()

        user_normal = User(full_name="normal",email="normal@email.com", hashed_password=pwd_context.hash("normal"))
        user_superadmin = User(full_name="superadmin",email="superadmin@email.com", hashed_password=pwd_context.hash("superadmin"))

        session.add_all([user_normal, user_superadmin])
        session.commit()

        role_user1 = RoleUser(role_id=role_user.id, user_id=user_normal.id,
                              remark="Blue wrote chapter 1")
        role_user2 = RoleUser(role_id=role_moderator.id, user_id=user_normal.id,
                              remark="Chip wrote chapter 2")
        role_user3 = RoleUser(role_id=role_moderator.id, user_id=user_superadmin.id,
                              remark="Blue wrote chapters 1-3")
        role_user4 = RoleUser(role_id=role_admin.id, user_id=user_superadmin.id,
                              remark="Alyssa wrote chapter 4")
        session.add_all([role_user1, role_user2, role_user3, role_user4])
        session.commit()
    finally:
        session.close()


init()
