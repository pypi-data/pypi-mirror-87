from django.contrib import admin
from .models import Profile, WeightRecord, LiftRecord, Food

admin.site.register(Profile)
admin.site.register(WeightRecord)
admin.site.register(LiftRecord)
admin.site.register(Food)
