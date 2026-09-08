from django.db import models
from django.contrib.auth.models import User

class TripBooking(models.Model):
    TRANSPORT_CHOICES = [
        ('train', 'Train'),
        ('bus', 'Bus'),
        ('flight', 'Flight'),
        ('car', 'Car'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    from_place = models.CharField(max_length=100)
    to_place = models.CharField(max_length=100)
    travel_date = models.DateField()
    transport_mode = models.CharField(max_length=10, choices=TRANSPORT_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.from_place} → {self.to_place} ({self.transport_mode})"

class Booking(models.Model):
    TRANSPORT_CHOICES = [
        ("train", "Train"),
        ("bus", "Bus"),
        ("flight", "Flight"),
        ("car", "Car"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    from_place = models.CharField(max_length=100)
    to_place = models.CharField(max_length=100)
    travel_date = models.DateField()
    transport_mode = models.CharField(max_length=20, choices=TRANSPORT_CHOICES)
    price = models.PositiveIntegerField()
    booked_on = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        default="Confirmed"
    )

    def __str__(self):
        return f"{self.user.username} - {self.from_place} → {self.to_place}"