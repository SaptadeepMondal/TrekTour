from functools import wraps
from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from models import Trek, Booking, User

staff = Blueprint("staff", __name__, url_prefix="/staff")


def staff_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for("auth.login"))
        if current_user.role != "staff":
            flash("Access Denied!", "danger")
            return redirect(url_for("auth.login"))
        if current_user.status != "approved":
            flash("Your account is awaiting admin approval.", "warning")
            return redirect(url_for("auth.login"))
        return func(*args, **kwargs)
    return wrapper


@staff.route("/dashboard")
@login_required
@staff_required
def staff_dashboard():

    assigned_treks = Trek.objects(assigned_staff=current_user.id, is_deleted=False)
    assigned_treks_count = assigned_treks.count()

    total_participants = Booking.objects(trek_id__in=assigned_treks).count()
    
    # Get recent active expeditions for the dashboard table
    recent_assigned = Trek.objects(assigned_staff=current_user.id, is_deleted=False).order_by('start_date').limit(5)

    return render_template(
        "staff/dashboard.html",
        assigned_treks=assigned_treks_count,
        total_participants=total_participants,
        recent_assigned=recent_assigned
    )


@staff.route("/treks/update/<id>", methods=["GET", "POST"])
@login_required
@staff_required
def update_trek(id):
    trek = Trek.objects(id=id).first()
    if not trek:
        abort(404)
        
    if trek.assigned_staff.id != current_user.id:
        flash("Access Denied!", "danger")
        return redirect(url_for("staff.assigned_treks"))
    
    booked_slots = Booking.objects(trek_id=trek.id, status="Booked").count()
    if request.method == "POST":
        try:
            available_slots = int(request.form["available_slots"])
            if available_slots < 0:
                flash("Available slots cannot be negative.", "danger")
                return render_template("staff/edit_trek.html", trek=trek, booked_slots=booked_slots)
            
            max_allowed_available = trek.total_slots - booked_slots
            if available_slots > max_allowed_available:
                flash(f"Available slots cannot exceed {max_allowed_available} (Total Slots minus current active bookings).", "danger")
                return render_template("staff/edit_trek.html", trek=trek, booked_slots=booked_slots)
            
            trek.available_slots = available_slots
            new_status = request.form["status"]
            trek.status = new_status
            
            if new_status == "Completed":
                for booking in trek.bookings:
                    if booking.status == "Booked":
                        booking.status = "Completed"
                        booking.save()
            
            trek.save()
            flash("Trek updated successfully.", "success")
            return redirect(url_for("staff.assigned_treks"))
        except ValueError:
            flash("Invalid slots format.", "danger")
            return render_template("staff/edit_trek.html", trek=trek, booked_slots=booked_slots)
    return render_template(
        "staff/edit_trek.html",
        trek=trek,
        booked_slots=booked_slots
    )


@staff.route("/treks")
@login_required
@staff_required
def assigned_treks():
    treks = Trek.objects(assigned_staff=current_user.id)
    return render_template(
        "staff/assigned_treks.html",
        treks=treks
    )


@staff.route("/participants/<id>")
@login_required
@staff_required
def participants(id):
    trek = Trek.objects(id=id).first()
    if not trek:
        abort(404)
        
    if trek.assigned_staff.id != current_user.id:
        flash("Access Denied!", "danger")
        return redirect(url_for("staff.assigned_treks"))
        
    bookings = Booking.objects(trek_id=id)
    return render_template(
        "staff/participants.html",
        trek=trek,
        bookings=bookings
    )