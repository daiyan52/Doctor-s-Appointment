from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class VaccinationCenter(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()
    working_hours = models.CharField(max_length=100)
    total_slots_per_day = models.IntegerField(default=10)
    total_dosage_given = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class VaccinationSlot(models.Model):
    SLOT_TIMES = [
        ("09:00", "09:00 AM - 10:00 AM"),
        ("10:00", "10:00 AM - 11:00 AM"),
        ("11:00", "11:00 AM - 12:00 PM"),
        ("12:00", "12:00 PM - 01:00 PM"),
        ("01:00", "01:00 PM - 02:00 PM"),
        ("02:00", "02:00 PM - 03:00 PM"),
        ("03:00", "03:00 PM - 04:00 PM"),
        ("04:00", "04:00 PM - 05:00 PM"),
    ]

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("confirmed", "Confirmed"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vaccination_center = models.ForeignKey(VaccinationCenter, on_delete=models.CASCADE)
    date = models.DateField()
    slot_time = models.CharField(max_length=5, choices=SLOT_TIMES)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pending")

    def __str__(self):
        return f"{self.user.username} - {self.vaccination_center.name} on {self.date} at {self.slot_time}"

    def clean(self):
        # Limit the number of bookings per day
        slots_count = VaccinationSlot.objects.filter(
            vaccination_center=self.vaccination_center,
            date=self.date,
        ).count()

        if slots_count >= self.vaccination_center.total_slots_per_day:
            raise ValidationError(
                f"No slots available for {self.date} at {self.vaccination_center.name}"
            )

    class Meta:
        unique_together = ("vaccination_center", "date", "slot_time")
