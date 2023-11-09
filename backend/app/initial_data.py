#!/usr/bin/env python3

from app.crud.user_crud import create_user, get_user_by_email
from app.schemas.user_schemas import UserCreate
from app.db.session import SessionLocal


def init() -> None:
    db = SessionLocal()
    user = get_user_by_email(db, "admin@scdao-api.org")
    if(user == None):
        print("No user is created beforehand")
        print("Creating superuser admin@scda-api.org")
        create_user(
            db,
            UserCreate(
                email="admin@scdao-api.org",
                password="password",
                is_active=True,
                is_superuser=True,
                is_county_authorized=True
            ),
        )
    else:
        print("A user is already create: " + user.email)


if __name__ == "__main__":
    print("Creating user...")
    init()
    print("Superuser created")
