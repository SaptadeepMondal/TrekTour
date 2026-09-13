from functools import wraps
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import User, Trek, Booking
from datetime import datetime, date
from mongoengine.queryset.visitor import Q
from flask import abort

class DummyTrek:
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            if k in ['total_slots', 'available_slots', 'duration'] and v is not None:
                try:
                    v = int(v)
                except (ValueError, TypeError):
                    v = 0
            setattr(self, k, v)


admin = Blueprint("admin",__name__,url_prefix="/admin")

def admin_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for("auth.login"))
        if current_user.role != "admin":
            flash("Access Denied!", "danger")
            return redirect(url_for("auth.login"))
        return func(*args, **kwargs)
    return wrapper

@admin.route("/dashboard")
@login_required
@admin_required
def admin_dashboard():
    total_users = User.objects(role="user").count()
    total_staff = User.objects(role="staff").count()
    total_treks = Trek.objects.count()
    total_bookings = Booking.objects.count()
    pending_staff = User.objects(role="staff", status="pending").count()
    recent_bookings = Booking.objects.order_by('-booking_date').limit(10)

    return render_template(
        "admin/dashboard.html",
        total_users=total_users,
        total_staff=total_staff,
        total_treks=total_treks,
        total_bookings=total_bookings,
        pending_staff=pending_staff,
        recent_bookings=recent_bookings
    )

@admin.route("/users")
@login_required
@admin_required
def users():
    search = request.args.get("search", "")
    if search:
        users = User.objects(role="user", name__icontains=search)
    else:
        users = User.objects(role="user")
    return render_template("admin/users.html",users=users,search=search)

@admin.route("/users/blacklist/<id>")
@login_required
@admin_required
def blacklist_user(id):
    user = User.objects(id=id).first()
    if not user: abort(404)
    user.status = "blacklisted"
    user.save()
    flash("User blacklisted.", "warning")
    return redirect(url_for("admin.users"))

@admin.route("/users/unblacklist/<id>")
@login_required
@admin_required
def unblacklist_user(id):
    user = User.objects(id=id).first()
    if not user: abort(404)
    user.status = "approved"
    user.save()
    flash("User restored.", "success")
    return redirect(url_for("admin.users"))

@admin.route("/staff")
@login_required
@admin_required
def staff():
    search = request.args.get("search", "")
    if search:
        staff = User.objects(role="staff", name__icontains=search)
    else:
        staff = User.objects(role="staff")
    return render_template("admin/staff.html", staff=staff, search=search)

@admin.route("/staff/approve/<id>")
@login_required
@admin_required
def approve_staff(id):
    staff = User.objects(id=id).first()
    if not staff: abort(404)
    staff.status = "approved"
    staff.save()
    flash("Staff approved successfully.", "success")
    return redirect(url_for("admin.staff"))

@admin.route("/staff/blacklist/<id>")
@login_required
@admin_required
def blacklist_staff(id):
    staff = User.objects(id=id).first()
    if not staff: abort(404)
    staff.status = "blacklisted"
    staff.save()
    flash("Staff blacklisted.", "warning")
    return redirect(url_for("admin.staff"))

@admin.route("/staff/unblacklist/<id>")
@login_required
@admin_required
def unblacklist_staff(id):
    staff = User.objects(id=id).first()
    if not staff: abort(404)
    staff.status = "approved"
    staff.save()
    flash("Staff restored successfully.", "success")
    return redirect(url_for("admin.staff"))

@admin.route("/treks")
@login_required
@admin_required
def treks():
    search = request.args.get("search", "")
    if search:
        treks = Trek.objects(name__icontains=search)
    else:
        treks = Trek.objects()
    return render_template("admin/treks.html", treks=treks, search=search)

@admin.route("/treks/add", methods=["GET", "POST"])
@login_required
@admin_required
def add_trek():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        location = request.form.get("location", "").strip()
        difficulty = request.form.get("difficulty", "Easy")
        duration_str = request.form.get("duration", "")
        total_slots_str = request.form.get("total_slots", "")
        available_slots_str = request.form.get("available_slots", "")
        start_date_str = request.form.get("start_date", "")
        end_date_str = request.form.get("end_date", "")
        description = request.form.get("description", "").strip()

        temp_trek = DummyTrek(
            name=name, location=location, difficulty=difficulty,
            duration=duration_str, total_slots=total_slots_str,
            available_slots=available_slots_str, start_date=start_date_str,
            end_date=end_date_str, description=description
        )
        if not name:
            flash("Trek Name cannot be empty.", "danger")
            return render_template("admin/trek_form.html", trek=temp_trek)
        if not location:
            flash("Location cannot be empty.", "danger")
            return render_template("admin/trek_form.html", trek=temp_trek)
        if not description:
            flash("Description cannot be empty.", "danger")
            return render_template("admin/trek_form.html", trek=temp_trek)
        if difficulty not in ["Easy", "Moderate", "Hard"]:
            flash("Invalid difficulty level selection.", "danger")
            return render_template("admin/trek_form.html", trek=temp_trek)

        try:
            duration = int(duration_str)
            total_slots = int(total_slots_str)
            available_slots = int(available_slots_str)
        except ValueError:
            flash("Duration, Total Slots, and Available Slots must be valid integers.", "danger")
            return render_template("admin/trek_form.html", trek=temp_trek)

        if duration <= 0:
            flash("Duration must be at least 1 day.", "danger")
            return render_template("admin/trek_form.html", trek=temp_trek)
        if total_slots <= 0:
            flash("Total Slots must be at least 1.", "danger")
            return render_template("admin/trek_form.html", trek=temp_trek)
        if available_slots < 0:
            flash("Available Slots cannot be negative.", "danger")
            return render_template("admin/trek_form.html", trek=temp_trek)
        if available_slots > total_slots:
            flash("Available Slots cannot exceed Total Slots.", "danger")
            return render_template("admin/trek_form.html", trek=temp_trek)

        try:
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
        except ValueError:
            flash("Invalid date format. Use YYYY-MM-DD.", "danger")
            return render_template("admin/trek_form.html", trek=temp_trek)

        if start_date.date() < date.today():
            flash("Start Date cannot be in the past.", "danger")
            return render_template("admin/trek_form.html", trek=temp_trek)
        if end_date <= start_date:
            flash("End Date must be after the Start Date.", "danger")
            return render_template("admin/trek_form.html", trek=temp_trek)
        if duration != (end_date - start_date).days:
            flash(f"Duration must match the difference between Start and End dates ({(end_date - start_date).days} days).", "danger")
            return render_template("admin/trek_form.html", trek=temp_trek)

        trek = Trek(
            name=name, location=location, difficulty=difficulty,
            duration=duration, total_slots=total_slots,
            available_slots=available_slots, start_date=start_date,
            end_date=end_date, description=description
        )
        trek.save()
        flash("Trek added successfully.", "success")
        return redirect(url_for("admin.treks"))
    return render_template("admin/trek_form.html", trek=None)

@admin.route("/treks/assign/<id>", methods=["GET", "POST"])
@login_required
@admin_required
def assign_staff(id):
    trek = Trek.objects(id=id).first()
    if not trek: abort(404)
    staff_list = User.objects(role="staff", status="approved")

    if request.method == "POST":
        staff_id = request.form.get("staff_id")
        if staff_id:
            staff_user = User.objects(id=staff_id).first()
            trek.assigned_staff = staff_user
        else:
            trek.assigned_staff = None
        trek.save()
        flash("Staff assigned successfully.", "success")
        return redirect(url_for("admin.treks"))

    return render_template("admin/assign_staff.html", trek=trek, staff_list=staff_list)


@admin.route("/treks/edit/<id>", methods=["GET", "POST"])
@login_required
@admin_required
def edit_trek(id):
    trek = Trek.objects(id=id).first()
    if not trek: abort(404)
    booked_slots = Booking.objects(trek_id=trek.id, status="Booked").count()
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        location = request.form.get("location", "").strip()
        difficulty = request.form.get("difficulty", "Easy")
        duration_str = request.form.get("duration", "")
        total_slots_str = request.form.get("total_slots", "")
        available_slots_str = request.form.get("available_slots", "")
        start_date_str = request.form.get("start_date", "")
        end_date_str = request.form.get("end_date", "")
        description = request.form.get("description", "").strip()

        temp_trek = DummyTrek(
            id=str(trek.id), name=name, location=location, difficulty=difficulty,
            duration=duration_str, total_slots=total_slots_str,
            available_slots=available_slots_str, start_date=start_date_str,
            end_date=end_date_str, description=description
        )

        if not name:
            flash("Trek Name cannot be empty.", "danger")
            return render_template("admin/trek_form.html", trek=temp_trek, booked_slots=booked_slots)
        if not location:
            flash("Location cannot be empty.", "danger")
            return render_template("admin/trek_form.html", trek=temp_trek, booked_slots=booked_slots)
        if not description:
            flash("Description cannot be empty.", "danger")
            return render_template("admin/trek_form.html", trek=temp_trek, booked_slots=booked_slots)
        if difficulty not in ["Easy", "Moderate", "Hard"]:
            flash("Invalid difficulty level selection.", "danger")
            return render_template("admin/trek_form.html", trek=temp_trek, booked_slots=booked_slots)

        try:
            duration = int(duration_str)
            total_slots = int(total_slots_str)
            available_slots = int(available_slots_str)
        except ValueError:
            flash("Duration, Total Slots, and Available Slots must be valid integers.", "danger")
            return render_template("admin/trek_form.html", trek=temp_trek, booked_slots=booked_slots)

        if duration <= 0:
            flash("Duration must be at least 1 day.", "danger")
            return render_template("admin/trek_form.html", trek=temp_trek, booked_slots=booked_slots)
        if total_slots <= 0:
            flash("Total Slots must be at least 1.", "danger")
            return render_template("admin/trek_form.html", trek=temp_trek, booked_slots=booked_slots)
        if available_slots < 0:
            flash("Available Slots cannot be negative.", "danger")
            return render_template("admin/trek_form.html", trek=temp_trek, booked_slots=booked_slots)
        if available_slots > total_slots:
            flash("Available Slots cannot exceed Total Slots.", "danger")
            return render_template("admin/trek_form.html", trek=temp_trek, booked_slots=booked_slots)

        if total_slots < booked_slots:
            flash(f"Total Slots ({total_slots}) cannot be less than current active bookings ({booked_slots}).", "danger")
            return render_template("admin/trek_form.html", trek=temp_trek, booked_slots=booked_slots)

        max_allowed_available = total_slots - booked_slots
        if available_slots > max_allowed_available:
            flash(f"Available Slots ({available_slots}) cannot exceed {max_allowed_available} (Total Slots minus current active bookings).", "danger")
            return render_template("admin/trek_form.html", trek=temp_trek, booked_slots=booked_slots)

        try:
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
        except ValueError:
            flash("Invalid date format. Use YYYY-MM-DD.", "danger")
            return render_template("admin/trek_form.html", trek=temp_trek, booked_slots=booked_slots)

        if end_date <= start_date:
            flash("End Date must be after the Start Date.", "danger")
            return render_template("admin/trek_form.html", trek=temp_trek, booked_slots=booked_slots)
        if duration != (end_date - start_date).days:
            flash(f"Duration must match the difference between Start and End dates ({(end_date - start_date).days} days).", "danger")
            return render_template("admin/trek_form.html", trek=temp_trek, booked_slots=booked_slots)

        if start_date != trek.start_date and start_date.date() < date.today():
            flash("New Start Date cannot be in the past.", "danger")
            return render_template("admin/trek_form.html", trek=temp_trek, booked_slots=booked_slots)

        trek.name = name
        trek.location = location
        trek.difficulty = difficulty
        trek.duration = duration
        trek.total_slots = total_slots
        trek.available_slots = available_slots
        trek.start_date = start_date
        trek.end_date = end_date
        trek.description = description
        trek.save()
        flash("Trek updated successfully.", "success")
        return redirect(url_for("admin.treks"))
    return render_template("admin/trek_form.html", trek=trek, booked_slots=booked_slots)

@admin.route("/treks/delete/<id>")
@login_required
@admin_required
def delete_trek(id):
    trek = Trek.objects(id=id).first()
    if not trek: abort(404)
    trek.is_deleted = True
    trek.save()
    flash("Trek removed.", "warning")
    return redirect(url_for("admin.treks"))

@admin.route("/treks/restore/<id>")
@login_required
@admin_required
def restore_trek(id):
    trek = Trek.objects(id=id).first()
    if not trek: abort(404)
    trek.is_deleted = False
    trek.save()
    flash("Trek restored.", "success")
    return redirect(url_for("admin.treks"))

@admin.route("/bookings")
@login_required
@admin_required
def bookings():
    search = request.args.get("search", "")
    if search:
        matching_users = User.objects(name__icontains=search)
        matching_treks = Trek.objects(name__icontains=search)
        bookings = Booking.objects(Q(user_id__in=matching_users) | Q(trek_id__in=matching_treks)).order_by('-booking_date')
    else:
        bookings = Booking.objects.order_by('-booking_date')
    return render_template("admin/bookings.html", bookings=bookings, search=search)