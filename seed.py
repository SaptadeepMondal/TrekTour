import random
from datetime import date, datetime, timedelta
from werkzeug.security import generate_password_hash
from app import app
from models import User, Trek, Booking


with app.app_context():
    Booking.objects().delete()
    Trek.objects().delete()
    User.objects(role__ne="admin").delete()
    print("Old data cleared.")

    staff_names = [
        "Rahul",
        "Amit",
        "Priya",
        "Sneha",
        "Rohit"
    ]

    staff_members = []
    for i, name in enumerate(staff_names, start=1):
        staff = User(
            username=f"staff{i}",
            name=name,
            email=f"staff{i}@trek.com",
            phone=f"98765432{i:02}",
            password=generate_password_hash("staff123"),
            role="staff",
            status="approved"
        )
        staff.save()
        staff_members.append(staff)

    print("Staff Created")



    first_names = [
        "Arjun","Neha","Karan","Riya","Ankit",
        "Soham","Ananya","Aisha","Vikram","Meera",
        "Rohan","Diya","Aman","Pooja","Ishaan",
        "Kabir","Nisha","Dev","Tina","Yash"
    ]

    users = []
    for i, name in enumerate(first_names, start=1):
        user = User(
            username=f"user{i}",
            name=name,
            email=f"user{i}@gmail.com",
            phone=f"900000{i:04}",
            password=generate_password_hash("user123"),
            role="user",
            status="approved"
        )
        user.save()
        users.append(user)
    
    print("Users Created")



    trek_data = [
        ("Sandakphu", "West Bengal", "Hard"),
        ("Kedarkantha", "Uttarakhand", "Easy"),
        ("Hampta Pass", "Himachal Pradesh", "Moderate"),
        ("Triund", "Himachal Pradesh", "Easy"),
        ("Valley of Flowers", "Uttarakhand", "Moderate"),
        ("Tarsar Marsar", "Kashmir", "Hard"),
        ("Goechala", "Sikkim", "Hard"),
        ("Brahmatal", "Uttarakhand", "Moderate"),
        ("Nag Tibba", "Uttarakhand", "Easy"),
        ("Dzongri", "Sikkim", "Moderate")

    ]
    treks = []
    for i, trek in enumerate(trek_data):
        total = random.randint(20, 40)
        start = datetime.utcnow() + timedelta(days=random.randint(5, 90))
        end = start + timedelta(days=random.randint(2, 8))
        obj = Trek(
            name=trek[0],
            location=trek[1],
            difficulty=trek[2],
            duration=(end - start).days,
            total_slots=total,
            available_slots=total,
            assigned_staff=random.choice(staff_members),
            start_date=start,
            end_date=end,
            status="Open",
            description=f"Experience the beauty of {trek[0]}."

        )
        obj.save()
        treks.append(obj)
    
    print("Treks Created")



    for user in users:
        booked = random.sample(
            treks,
            random.randint(1, 3)
        )

        for trek in booked:
            if trek.available_slots <= 0:
                continue

            booking = Booking(
                user_id=user,
                trek_id=trek,
                booking_date=datetime.utcnow() - timedelta(
                    days=random.randint(1, 30)
                ),
                number_of_people=1,
                status="Booked"
            )

            trek.available_slots -= 1
            trek.save()
            booking.save()
            
    print("Bookings Created")
    print("\nDatabase Seeded Successfully!")