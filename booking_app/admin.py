from django.contrib import admin
from booking_app.models import VaccinationCenter, VaccinationSlot

@admin.register(VaccinationCenter)
class VaccinationCenterAdmin(admin.ModelAdmin):
    pass

@admin.register(VaccinationSlot)
class VaccinationSlotAdmin(admin.ModelAdmin):
    pass
