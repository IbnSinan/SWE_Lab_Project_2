"""
models.py
Database schema for the Municipal Waste Billing System MVP.

Entities:
    User      - staff/admin login (used by the auth module - 2203136)
    Resident  - household/holding registered for waste collection (2203138)
    Bill      - a waste collection bill issued to a resident (2203138)
"""
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import db


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default="staff")  # staff / admin
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, raw_password):
        self.password_hash = generate_password_hash(raw_password)

    def check_password(self, raw_password):
        return check_password_hash(self.password_hash, raw_password)

    def __repr__(self):
        return f"<User {self.username}>"


class Resident(db.Model):
    __tablename__ = "residents"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    holding_number = db.Column(db.String(30), unique=True, nullable=False)
    address = db.Column(db.String(200), nullable=False)
    phone = db.Column(db.String(20))
    category = db.Column(db.String(20), default="Household")  # Household / Commercial
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    bills = db.relationship("Bill", backref="resident", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Resident {self.name}>"


class Bill(db.Model):
    __tablename__ = "bills"

    id = db.Column(db.Integer, primary_key=True)
    resident_id = db.Column(db.Integer, db.ForeignKey("residents.id"), nullable=False)
    billing_month = db.Column(db.String(20), nullable=False)   # e.g. "August 2026"
    amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(10), default="Unpaid")        # Unpaid / Paid
    due_date = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Bill {self.id} - {self.status}>"
