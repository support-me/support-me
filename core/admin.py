from django.contrib import admin
from core.models import Profile, BraFitting
# Register your models here.

@admin.register(BraFitting)
class BraFittingAdmin(admin.ModelAdmin):
    pass

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    pass