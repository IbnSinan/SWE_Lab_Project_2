"""
api/routes.py
--------------------------------------------------------
Module owner : 2203138
Feature branch: feature/backend-module
--------------------------------------------------------
Core backend REST API: resident CRUD, waste-bill CRUD, and the
dashboard summary endpoint that the frontend (2203137) calls
with fetch(). Every route is protected by the login_required
guard from the auth module (2203136).
"""
from flask import Blueprint, request, jsonify

from extensions import db
from models import Resident, Bill
from auth.routes import login_required

api_bp = Blueprint("api", __name__, url_prefix="/api")


def resident_to_dict(r):
    return {
        "id": r.id,
        "name": r.name,
        "holding_number": r.holding_number,
        "address": r.address,
        "phone": r.phone,
        "category": r.category,
    }


def bill_to_dict(b):
    return {
        "id": b.id,
        "resident_id": b.resident_id,
        "resident_name": b.resident.name,
        "billing_month": b.billing_month,
        "amount": b.amount,
        "status": b.status,
        "due_date": b.due_date,
    }


# ---------- Resident CRUD ----------

@api_bp.route("/residents", methods=["GET"])
@login_required
def list_residents():
    residents = Resident.query.order_by(Resident.id.desc()).all()
    return jsonify([resident_to_dict(r) for r in residents])


@api_bp.route("/residents/<int:resident_id>", methods=["GET"])
@login_required
def get_resident(resident_id):
    resident = Resident.query.get_or_404(resident_id)
    return jsonify(resident_to_dict(resident))


@api_bp.route("/residents", methods=["POST"])
@login_required
def create_resident():
    data = request.get_json(silent=True) or {}

    if not data.get("name") or not data.get("holding_number") or not data.get("address"):
        return jsonify({"error": "name, holding_number and address are required."}), 400

    if Resident.query.filter_by(holding_number=data.get("holding_number")).first():
        return jsonify({"error": "A resident with this holding number already exists."}), 409

    resident = Resident(
        name=data.get("name", "").strip(),
        holding_number=data.get("holding_number", "").strip(),
        address=data.get("address", "").strip(),
        phone=(data.get("phone") or "").strip(),
        category=data.get("category", "Household"),
    )
    db.session.add(resident)
    db.session.commit()
    return jsonify(resident_to_dict(resident)), 201


@api_bp.route("/residents/<int:resident_id>", methods=["PUT"])
@login_required
def update_resident(resident_id):
    resident = Resident.query.get_or_404(resident_id)
    data = request.get_json(silent=True) or {}

    resident.name = (data.get("name") or resident.name).strip()
    resident.holding_number = (data.get("holding_number") or resident.holding_number).strip()
    resident.address = (data.get("address") or resident.address).strip()
    resident.phone = data.get("phone", resident.phone)
    resident.category = data.get("category", resident.category)
    db.session.commit()
    return jsonify(resident_to_dict(resident))


@api_bp.route("/residents/<int:resident_id>", methods=["DELETE"])
@login_required
def delete_resident(resident_id):
    resident = Resident.query.get_or_404(resident_id)
    db.session.delete(resident)
    db.session.commit()
    return jsonify({"message": "Resident removed."})


# ---------- Bill CRUD ----------

@api_bp.route("/bills", methods=["GET"])
@login_required
def list_bills():
    bills = Bill.query.order_by(Bill.id.desc()).all()
    return jsonify([bill_to_dict(b) for b in bills])


@api_bp.route("/bills", methods=["POST"])
@login_required
def create_bill():
    data = request.get_json(silent=True) or {}
    resident_id = data.get("resident_id")

    if not resident_id or not Resident.query.get(resident_id):
        return jsonify({"error": "A valid resident_id is required."}), 400

    try:
        amount = float(data.get("amount", 0))
    except (TypeError, ValueError):
        return jsonify({"error": "amount must be a number."}), 400

    bill = Bill(
        resident_id=resident_id,
        billing_month=(data.get("billing_month") or "").strip(),
        amount=amount,
        due_date=(data.get("due_date") or "").strip(),
        status="Unpaid",
    )
    db.session.add(bill)
    db.session.commit()
    return jsonify(bill_to_dict(bill)), 201


@api_bp.route("/bills/<int:bill_id>/toggle-status", methods=["PATCH"])
@login_required
def toggle_bill_status(bill_id):
    bill = Bill.query.get_or_404(bill_id)
    bill.status = "Paid" if bill.status == "Unpaid" else "Unpaid"
    db.session.commit()
    return jsonify(bill_to_dict(bill))


@api_bp.route("/bills/<int:bill_id>", methods=["DELETE"])
@login_required
def delete_bill(bill_id):
    bill = Bill.query.get_or_404(bill_id)
    db.session.delete(bill)
    db.session.commit()
    return jsonify({"message": "Bill deleted."})


# ---------- Dashboard summary ----------

@api_bp.route("/dashboard/summary", methods=["GET"])
@login_required
def dashboard_summary():
    total_residents = Resident.query.count()
    total_bills = Bill.query.count()
    unpaid_bills = Bill.query.filter_by(status="Unpaid").all()
    paid_bills = Bill.query.filter_by(status="Paid").all()
    recent_bills = Bill.query.order_by(Bill.id.desc()).limit(5).all()

    return jsonify({
        "total_residents": total_residents,
        "total_bills": total_bills,
        "unpaid_count": len(unpaid_bills),
        "paid_count": len(paid_bills),
        "total_due": sum(b.amount for b in unpaid_bills),
        "total_collected": sum(b.amount for b in paid_bills),
        "recent_bills": [bill_to_dict(b) for b in recent_bills],
    })