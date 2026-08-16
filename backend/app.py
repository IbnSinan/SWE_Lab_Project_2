"""
app.py
--------------------------------------------------------
Application factory / entry point.
Wires together the auth API (2203136) and the backend API
(2203138) as Flask blueprints, serves the static frontend
(2203137) straight from the ../frontend folder, and creates
the SQLite database with a default admin account plus a
little demo data so the MVP is ready to click through.

Run with:
    python app.py
Then open http://127.0.0.1:5000 in a browser.
Default login -> username: admin   password: admin123
"""
import os
from flask import Flask, send_from_directory

from extensions import db
from models import User, Resident, Bill

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(os.path.dirname(BASE_DIR), "frontend")


def create_app():
    app = Flask(__name__, static_folder=FRONTEND_DIR, static_url_path="")
    app.config["SECRET_KEY"] = "dev-secret-key-change-in-production"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///waste_billing.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    from auth.routes import auth_bp
    from api.routes import api_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(api_bp)

    @app.route("/")
    def index():
        return send_from_directory(FRONTEND_DIR, "index.html")

    with app.app_context():
        db.create_all()
        _seed_default_admin()
        _seed_demo_data()

    return app


def _seed_default_admin():
    if User.query.filter_by(username="admin").first() is None:
        admin = User(username="admin", role="admin")
        admin.set_password("admin123")
        db.session.add(admin)
        db.session.commit()


def _seed_demo_data():
    """A couple of sample residents/bills so the MVP isn't empty on first run."""
    if Resident.query.count() == 0:
        r1 = Resident(
            name="Md. Kamal Hossain",
            holding_number="RCC-W12-0451",
            address="House 14, Road 3, Ward No. 12, Rajshahi City Corporation",
            phone="01712345678",
            category="Household",
        )
        r2 = Resident(
            name="Fatema Traders",
            holding_number="RCC-W07-0118",
            address="Shop 22, Shaheb Bazar, Ward No. 07, Rajshahi City Corporation",
            phone="01898765432",
            category="Commercial",
        )
        db.session.add_all([r1, r2])
        db.session.commit()

        db.session.add(Bill(resident_id=r1.id, billing_month="July 2026", amount=150.0,
                             due_date="2026-08-10", status="Paid"))
        db.session.add(Bill(resident_id=r2.id, billing_month="July 2026", amount=450.0,
                             due_date="2026-08-10", status="Unpaid"))
        db.session.commit()


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
