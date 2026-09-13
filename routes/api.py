from flask import Blueprint, jsonify, abort
from models import User, Trek, Booking

api = Blueprint("api", __name__, url_prefix="/api")


@api.route("/treks")
def get_all_treks():
    treks = Trek.objects()
    return jsonify([
        {
            "id": str(trek.id),
            "name": trek.name,
            "location": trek.location,
            "difficulty": trek.difficulty,
            "duration": trek.duration,
            "total_slots": trek.total_slots,
            "available_slots": trek.available_slots,
            "assigned_staff": str(trek.assigned_staff.id) if trek.assigned_staff else None,
            "start_date": str(trek.start_date),
            "end_date": str(trek.end_date),
            "status": trek.status,
            "description": trek.description
        }
        for trek in treks
    ])


@api.route("/treks/<id>")
def get_single_trek(id):
    trek = Trek.objects(id=id).first()
    if not trek: abort(404)
    return jsonify(
        {
            "id": str(trek.id),
            "name": trek.name,
            "location": trek.location,
            "difficulty": trek.difficulty,
            "duration": trek.duration,
            "total_slots": trek.total_slots,
            "available_slots": trek.available_slots,
            "assigned_staff": str(trek.assigned_staff.id) if trek.assigned_staff else None,
            "start_date": str(trek.start_date),
            "end_date": str(trek.end_date),
            "status": trek.status,
            "description": trek.description
        }
    )


@api.route("/users")
def get_users():
    users = User.objects(role="user")
    return jsonify([
        {
            "id": str(user.id),
            "username": user.username,
            "name": user.name,
            "email": user.email,
            "phone": user.phone,
            "status": user.status
        }
        for user in users
    ])


@api.route("/staff")
def get_staff():
    staff = User.objects(role="staff")
    return jsonify([
        {
            "id": str(member.id),
            "username": member.username,
            "name": member.name,
            "email": member.email,
            "phone": member.phone,
            "status": member.status
        }
        for member in staff
    ])


@api.route("/bookings")
def get_bookings():
    bookings = Booking.objects()
    return jsonify([
        {
            "id": str(booking.id),
            "user_id": str(booking.user_id.id) if booking.user_id else None,
            "trek_id": str(booking.trek_id.id) if booking.trek_id else None,
            "booking_date": str(booking.booking_date),
            "number_of_people": booking.number_of_people,
            "status": booking.status
        }
        for booking in bookings
    ])