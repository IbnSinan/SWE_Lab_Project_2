"""
auth/routes.py
--------------------------------------------------------
Module owner : 2203136
Feature branch: feature/auth-module
--------------------------------------------------------
REST API for staff authentication: register, login, logout,
and a session-check endpoint the frontend uses to guard pages.
Also exposes the login_required decorator reused by the
backend API module (2203138).

Session-based (cookie) auth - kept simple since this is a
first-milestone MVP, not a production system.
"""
from functools import wraps
from flask import Blueprint, request, session, jsonify

from extensions import db
from models import User

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")


def login_required(view_func):
    """Guard used by the backend API module (2203138) to protect routes."""
    @wraps(view_func)
    def wrapped_view(*args, **kwargs):
        if "user_id" not in session:
            return jsonify({"error": "Unauthorized. Please log in."}), 401
        return view_func(*args, **kwargs)
    return wrapped_view


@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json(silent=True) or {}
    username = (data.get("username") or "").strip()
    password = data.get("password") or ""

    if not username or not password:
        return jsonify({"error": "Username and password are required."}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({"error": "That username is already taken."}), 409

    user = User(username=username, role="staff")
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "Account created. Please log in."}), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json(silent=True) or {}
    username = (data.get("username") or "").strip()
    password = data.get("password") or ""

    user = User.query.filter_by(username=username).first()
    if not user or not user.check_password(password):
        return jsonify({"error": "Invalid username or password."}), 401

    session["user_id"] = user.id
    session["username"] = user.username
    return jsonify({"username": user.username, "role": user.role})


@auth_bp.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return jsonify({"message": "Logged out."})


@auth_bp.route("/session", methods=["GET"])
def check_session():
    if "user_id" in session:
        return jsonify({"logged_in": True, "username": session.get("username")})
    return jsonify({"logged_in": False})