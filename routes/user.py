from functools import wraps
from datetime import datetime

from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    flash,
    request,
    abort
)

from flask_login import login_required, current_user
from models import Trek, Booking
from mongoengine.queryset.visitor import Q

user = Blueprint("user",__name__,url_prefix="/user")


def user_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for("auth.login"))
        if current_user.role != "user":
            flash("Access Denied!", "danger")
            return redirect(url_for("auth.login"))
        if current_user.status != "approved":
            flash("Your account has been blacklisted or is not approved.", "danger")
            return redirect(url_for("auth.login"))
        return func(*args, **kwargs)
    return wrapper


@user.route("/dashboard")
@login_required
@user_required
def dashboard():
    active_treks = Trek.objects(is_deleted=False)
    total_bookings = Booking.objects(user_id=current_user.id, trek_id__in=active_treks).count()
    upcoming = Booking.objects(user_id=current_user.id, status="Booked", trek_id__in=active_treks).count()
    completed = Booking.objects(user_id=current_user.id, status="Completed", trek_id__in=active_treks).count()
    
    # Get recent bookings for the dashboard table
    recent_bookings = Booking.objects(user_id=current_user.id, trek_id__in=active_treks).order_by('-booking_date').limit(5)
    
    return render_template(
        "user/dashboard.html",
        total_bookings=total_bookings,
        upcoming=upcoming,
        completed=completed,
        recent_bookings=recent_bookings
    )


@user.route("/treks")
@login_required
@user_required
def treks():
    search = request.args.get("search", "")
    difficulty = request.args.get("difficulty", "")
    location = request.args.get("location", "")
    
    query = Q(status="Open") & Q(is_deleted=False)
    
    if search:
        query = query & Q(name__icontains=search)
    if difficulty:
        query = query & Q(difficulty=difficulty)
    if location:
        query = query & Q(location__icontains=location)
        
    treks = Trek.objects(query)
    
    return render_template(
        "user/treks.html",
        treks=treks,
        search=search,
        difficulty=difficulty,
        location=location
    )


@user.route("/book/<id>", methods=["POST"])
@login_required
@user_required
def book(id):
    trek = Trek.objects(id=id).first()
    if not trek:
        abort(404)
        
    if trek.status != "Open" or trek.is_deleted:
        flash("This trek is not available for booking.", "danger")
        return redirect(url_for("user.treks"))
    if trek.available_slots <= 0:
        flash("No slots available.", "danger")
        return redirect(url_for("user.treks"))
        
    existing = Booking.objects(user_id=current_user.id, trek_id=trek.id).first()

    if existing:
        flash("You have already booked this trek.", "warning")
        return redirect(url_for("user.treks"))
    else:
        booking = Booking(
            user_id=current_user._get_current_object(),
            trek_id=trek,
            booking_date=datetime.utcnow(),
            number_of_people=1,
            status="Booked"
        )
        trek.available_slots -= 1
        trek.save()
        booking.save()
        flash("Booking Successful!", "success")
        return redirect(url_for("user.bookings"))


@user.route("/bookings")
@login_required
@user_required
def bookings():
    active_treks = Trek.objects(is_deleted=False)
    bookings = Booking.objects(user_id=current_user.id, status__ne="Completed", trek_id__in=active_treks).order_by('-booking_date')
    return render_template(
        "user/bookings.html",
        bookings=bookings
    )


@user.route("/history")
@login_required
@user_required
def history():
    active_treks = Trek.objects(is_deleted=False)
    bookings = Booking.objects(user_id=current_user.id, status="Completed", trek_id__in=active_treks).order_by('-booking_date')
    return render_template(
        "user/history.html",
        bookings=bookings
    )


@user.route("/profile", methods=["GET", "POST"])
@login_required
@user_required
def profile():
    if request.method == "POST":
        current_user.name = request.form["name"]
        current_user.phone = request.form["phone"]
        current_user.email = request.form["email"]
        current_user.save()
        flash("Profile Updated!", "success")
        return redirect(url_for("user.profile"))
    return render_template(
        "user/profile.html"
    )