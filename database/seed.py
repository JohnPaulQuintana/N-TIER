from sqlalchemy import select

from configs.settings import settings
from database.connection import SessionLocal
from models.project import Project
from models.role import Role
from models.user import User
from models.user_project import UserProject
from utils.security import hash_password


ROLES = [
    {
        "name": "Administrator",
        "slug": "admin",
        "description": "Full access to the project.",
    },
    {
        "name": "User",
        "slug": "user",
        "description": "Standard project access.",
    },
    {
        "name": "Guest",
        "slug": "guest",
        "description": "Limited project access.",
    },
]


PROJECTS = [
    {
        "name": "Car Airconditioning",
        "slug": "car_airconditioning",
        "description": "Car airconditioning management system.",
    },
    {
        "name": "NaviLink",
        "slug": "navilink",
        "description": "Save, organize and navigate links.",
    },
    {
        "name": "GoBus",
        "slug": "gobus",
        "description": "Bus tracking and management system.",
    },
    {
        "name": "NaviTrack",
        "slug": "navitrack",
        "description": "Credits and loans tracker.",
    },
    {
        "name": "Risk Tool",
        "slug": "risk-tool",
        "description": "Risk management application.",
    },
]


def seed_roles(db):
    for role_data in ROLES:
        existing_role = db.scalar(
            select(Role).where(
                Role.slug == role_data["slug"],
            )
        )

        if existing_role:
            continue

        db.add(Role(**role_data))


def seed_projects(db):
    for project_data in PROJECTS:
        existing_project = db.scalar(
            select(Project).where(
                Project.slug == project_data["slug"],
            )
        )

        if existing_project:
            continue

        db.add(Project(**project_data))


def seed_admin(db):
    admin_role = db.scalar(
        select(Role).where(
            Role.slug == "admin",
        )
    )

    if not admin_role:
        raise ValueError("Admin role not found.")

    admin_user = db.scalar(
        select(User).where(
            User.email == settings.admin_email,
        )
    )

    if not admin_user:
        admin_user = User(
            email=settings.admin_email,
            password_hash=hash_password(
                settings.admin_password,
            ),
        )

        db.add(admin_user)
        db.flush()

    projects = db.scalars(
        select(Project).where(
            Project.is_active.is_(True),
        )
    ).all()

    for project in projects:
        existing_membership = db.scalar(
            select(UserProject).where(
                UserProject.user_id == admin_user.id,
                UserProject.project_id == project.id,
            )
        )

        if existing_membership:
            continue

        db.add(
            UserProject(
                user_id=admin_user.id,
                project_id=project.id,
                role_id=admin_role.id,
            )
        )


def seed():
    with SessionLocal() as db:
        seed_roles(db)
        seed_projects(db)

        # Make sure newly created roles/projects are available
        # before creating admin memberships.
        db.flush()

        seed_admin(db)

        db.commit()

        print("Database seed completed.")


if __name__ == "__main__":
    seed()