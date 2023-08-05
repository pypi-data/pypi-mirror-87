from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile
from .models import WeightRecord
from .models import LiftRecord
from .models import Food
from django.utils import timezone

WORKOUT_CATEGORIES = [
    ('All', 'All'),
    ('Abs', 'Abs'),
    ('Biceps', 'Biceps'),
    ('Butt/Hip', 'Butt/Hip'),
    ('Calves', 'Calves'),
    ('Chest', 'Chest'),
    ('Lats', 'Lats'),
    ('Shoulders', 'Shoulders'),
    ('Trapezius', 'Trapezius'),
    ('Triceps', 'Triceps'),
    ('Quads', 'Quads'),
]

MEAL_CATEGORIES = [
    ('All', 'All'),
    ('dinner-recipes', 'Dinner Recipes'),
    ('dessert', 'Dessert'),
    ('side-dishes', 'Sides'),
    ('appetizers', 'Appetizers'),
    ('breakfast-brunch', 'Breakfast & Brunch'),
    ('snacks', 'Snacks'),
    ('lunch', 'Lunch'),
    ('soup', 'Soup'),
    ('salad', 'Salad'),
    ('drinks', 'Drinks'),
    ]


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        #we probably want to change the labels of the fields on the front end
        #example: daily_cal_in = forms.IntegerField(label="Daily Calories")
        fields = ['daily_cal_in', 'daily_carbs', 'daily_fat', 'daily_protein','weight', 'goal_weight_change','activity_level']


class WeightForm(forms.ModelForm):
    class Meta:
        model = WeightRecord
        fields = ['lbs', 'date']


class LiftForm(forms.ModelForm):
    class Meta:
        model = LiftRecord
        fields = ['name','weight', 'sets', 'reps', 'date']


class ExerciseFilterForm(forms.Form):
    category = forms.CharField(label='Filter by Category: ', widget=forms.Select(choices = WORKOUT_CATEGORIES))
    

class FoodForm(forms.ModelForm):
    class Meta:
        model = Food
        fields = ['name','carbs', 'fats', 'protein', 'date']


class SingleFood(forms.Form):
    foodName = forms.CharField(label='Search for a specific food')
    date = forms.DateField(label='Date', initial=timezone.now)


class OptionForm(forms.Form):
    optionName = forms.ChoiceField()


class MealFilterForm(forms.Form):
    category = forms.CharField(label='Filter by Meal Type: ', widget=forms.Select(choices = MEAL_CATEGORIES))


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['activity_level', 'goal_weight_change']
