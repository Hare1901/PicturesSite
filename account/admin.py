from django.contrib import admin

from .models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):

    list_display = ['user', 'date_of_birds', 'photo']
    raw_id_fields = ['user']
