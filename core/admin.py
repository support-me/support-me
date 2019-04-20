from django.contrib import admin
from core.models import Profile, BraFitting, Suggestion, Resource
# Register your models here.

@admin.register(BraFitting)
class BraFittingAdmin(admin.ModelAdmin):
    pass

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    pass

@admin.register(Suggestion)
class SuggestionAdmin(admin.ModelAdmin):
    pass
@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    pass