from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile
from .models import WeightRecord
from .models import LiftRecord
import math

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=WeightRecord)
def save_weight(sender, instance, **kwargs):
    Profile.objects.filter(user=instance.user).update(weight=instance.lbs)

@receiver(post_save, sender=LiftRecord)
def calculate_one_rep_max(sender, instance, **kwargs):
    if instance.weight or instance.reps:
        one_rm = int(instance.weight) * (1+0.025*instance.reps)
        LiftRecord.objects.filter(user=instance.user, name=instance.name, date=instance.date).update(one_rep_max_equiv=one_rm)


@receiver(post_save, sender=Profile)
def recalculate_goals(sender, instance, **kwargs):
    current_weight = int(instance.weight)
    current_activity_level = float(instance.activity_level)
    current_weight_change = float(instance.goal_weight_change)

    new_daily_cals = current_weight*current_activity_level*10+current_weight_change*500
    new_pct_daily_prot = math.ceil((instance.weight *4/new_daily_cals)*100)
    new_pct_daily_carb = math.ceil((100-new_pct_daily_prot)*2/3)
    new_pct_daily_fat = math.floor((100-new_pct_daily_prot)/3)
    new_daily_prot = (new_pct_daily_prot/100)*new_daily_cals/4
    new_daily_carb = (new_pct_daily_carb/100)*new_daily_cals/4
    new_daily_fat = (new_pct_daily_fat/100)*new_daily_cals/9

    Profile.objects.filter(user=instance.user).update(daily_cal_in=new_daily_cals,
                                                      daily_carbs=new_daily_carb,
                                                      daily_fat=new_daily_fat,
                                                      daily_protein=new_daily_prot,
                                                      pct_diet_carbs=new_pct_daily_carb,
                                                      pct_diet_fat=new_pct_daily_fat,
                                                      pct_diet_prot=new_pct_daily_prot)
