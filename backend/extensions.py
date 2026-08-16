"""
extensions.py
Shared Flask extension instances.
Kept in its own module so both API blueprints (auth, api) can
import the same SQLAlchemy instance without circular imports.
"""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
