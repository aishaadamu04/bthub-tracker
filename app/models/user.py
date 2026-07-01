from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Parent:
    id: int
    full_name: str
    phone_number: str
    email: str
    password_hash: str
    created_at: str = field(default_factory=str)

    @staticmethod
    def from_row(row):
        """Convert a raw SQLite row into a Parent object."""
        return Parent(
            id=row['id'],
            full_name=row['full_name'],
            phone_number=row['phone_number'],
            email=row['email'],
            password_hash=row['password_hash'],
            created_at=row['created_at']
        )


@dataclass
class Child:
    id: int
    full_name: str
    username: str
    password_hash: str
    parent_phone: str
    current_level: int = 1
    created_at: str = field(default_factory=str)

    @staticmethod
    def from_row(row):
        """Convert a raw SQLite row into a Child object."""
        return Child(
            id=row['id'],
            full_name=row['full_name'],
            username=row['username'],
            password_hash=row['password_hash'],
            parent_phone=row['parent_phone'],
            current_level=row['current_level'],
            created_at=row['created_at']
        )
    

