from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy


def validate_activity_level(value):
    if value < 1.2 or value > 2.1:
        raise ValidationError(
            gettext_lazy(f'{value} is not in the range 1.2-2.1'),
            params={'value':value}
        )

def validate_goal_weight_change(value):
    if value < -1 or value > 1:
        raise ValidationError(
            gettext_lazy(f"{value} is not in the range (-1) - (1) "),
            params={'value': value}
        )

def validate_not_neg(value):
    if value < 0:
        raise ValidationError(
            gettext_lazy(f"This value cannot be a negative number"),
            params={'value': value}
        )


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(default='default.jpg', upload_to='profile_pics')
    daily_cal_in = models.IntegerField(default=2000)
    daily_carbs = models.IntegerField(default=0)
    daily_fat = models.IntegerField(default=0)
    daily_protein = models.IntegerField(default=0)
    weight = models.IntegerField(default=150)
    pct_diet_carbs = models.IntegerField(default=45)
    pct_diet_fat = models.IntegerField(default=20)
    pct_diet_prot = models.IntegerField(default=35)
    goal_weight_change = models.DecimalField(max_digits=3, decimal_places=2, default=-1,
                                             help_text="Must be a value between -1 and 1", validators=[validate_goal_weight_change])
    activity_level = models.DecimalField(max_digits=2, decimal_places=1,default=1.5,
                                         help_text="Must be a value between 1.2 and 2.1",
                                         validators=[validate_activity_level])
    def __str__(self):
        return f'{self.user.username} Profile'


class WeightRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lbs = models.IntegerField(help_text='May not be a negative number.',
                              validators=[validate_not_neg])
    date = models.DateField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username}: {self.lbs} on {self.date}"


class LiftRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    weight = models.IntegerField(blank=True, null=True, validators=[validate_not_neg], help_text="Cannot be negative")
    sets = models.IntegerField(blank=True, null=True, validators=[validate_not_neg], help_text="Cannot be negative")
    reps = models.IntegerField(blank=True, null=True, validators=[validate_not_neg], help_text="Cannot be negative")
    date = models.DateField(default=timezone.now)
    one_rep_max_equiv = models.IntegerField(blank=True, null=True)


class Food(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    carbs = models.IntegerField(validators=[validate_not_neg])
    fats = models.IntegerField(validators=[validate_not_neg])
    protein = models.IntegerField(validators=[validate_not_neg])
    calories = models.IntegerField(default=0, validators=[validate_not_neg])
    date = models.DateField(default=timezone.now)
