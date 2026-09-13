from mongoengine import Document, StringField, IntField, ReferenceField, BooleanField, DateTimeField
from flask_login import UserMixin
import datetime

class User(UserMixin, Document):
    meta = {'collection': 'user'}
    username = StringField(max_length=100, unique=True, required=True)
    email = StringField(max_length=100, unique=True, required=True)
    name = StringField(max_length=100, required=True)
    phone = StringField(max_length=20)
    password = StringField(max_length=255, required=True)
    role = StringField(max_length=20, default="user")
    status = StringField(max_length=20, default="approved")

    @property
    def bookings(self):
        return Booking.objects(user_id=self)

    def __repr__(self):
        return f"<User {self.username}>"


class Trek(Document):
    meta = {'collection': 'trek'}
    name = StringField(max_length=100, required=True)
    location = StringField(max_length=100, required=True)
    difficulty = StringField(max_length=50, required=True)
    duration = IntField(required=True)
    total_slots = IntField(required=True)
    available_slots = IntField(required=True)

    assigned_staff = ReferenceField(User)

    start_date = DateTimeField()
    end_date = DateTimeField()
    status = StringField(max_length=20, default="Pending")
    is_deleted = BooleanField(default=False)

    description = StringField()

    @property
    def bookings(self):
        return Booking.objects(trek_id=self)

    def __repr__(self):
        return f"<Trek {self.name}>"


class Booking(Document):
    meta = {'collection': 'booking'}
    user_id = ReferenceField(User, required=True)
    trek_id = ReferenceField(Trek, required=True)

    booking_date = DateTimeField(default=datetime.datetime.utcnow)

    number_of_people = IntField(default=1, required=True)
    status = StringField(max_length=20, default="Booked")

    @property
    def user(self):
        return self.user_id

    @property
    def trek(self):
        return self.trek_id

    def __repr__(self):
        return f"<Booking {self.id}>"