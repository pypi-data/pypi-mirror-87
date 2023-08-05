from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.utils.timezone import now, localtime
import json, os
from .forms import *
from .models import *
import io, matplotlib, urllib, base64
import re
import matplotlib.pyplot as plt
import datetime
from dateutil.parser import parse
import requests 
from bs4 import BeautifulSoup
import cchardet as chardet
import lxml
import concurrent.futures
import datetime
import math
import numpy as np


URLS = [
    {'Abs' : 'https://www.acefitness.org/education-and-resources/lifestyle/exercise-library/body-part/abs/'},
    {'Biceps' : 'https://www.acefitness.org/education-and-resources/lifestyle/exercise-library/body-part/arms/biceps/'},
    {'Butt/Hip' : 'https://www.acefitness.org/education-and-resources/lifestyle/exercise-library/body-part/butt-hips/'},
    {'Calves' : 'https://www.acefitness.org/education-and-resources/lifestyle/exercise-library/body-part/legs-calves-and-shins/soleus/'},
    {'Chest' : 'https://www.acefitness.org/education-and-resources/lifestyle/exercise-library/body-part/chest/'},
    {'Lats' : 'https://www.acefitness.org/education-and-resources/lifestyle/exercise-library/body-part/back/latissimus-dorsi(lats)/'},
    {'Shoulders' : 'https://www.acefitness.org/education-and-resources/lifestyle/exercise-library/body-part/shoulders/'},
    {'Trapezius' : 'https://www.acefitness.org/education-and-resources/lifestyle/exercise-library/body-part/back/trapezius(traps)/'},
    {'Triceps' : 'https://www.acefitness.org/education-and-resources/lifestyle/exercise-library/body-part/arms/triceps/'},
    {'Quads'  : 'https://www.acefitness.org/education-and-resources/lifestyle/exercise-library/body-part/legs-calves-and-shins/soleus/'}
]

MEALNAME = ""
EXERCISES_GLOBAL = []


def register(request):
    #If the user presses the register button the reqest methon will be POST
    if request.method == 'POST':
        #Creates a UserRegistrationForm with the information from the request which is associated with the user model in the database
        form = UserRegisterForm(request.POST)
        #Checks the validitiy of the information entered in the form
        if form.is_valid():
            #Saving adds the informaiton to the database
            new_user = form.save()
            messages.info(request, "Thanks for registering. You are now logged in.")
            new_user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
            login(request, new_user)
            return redirect('profile')
    else:
        #if there is not a POST request then display an empty form
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form' : form})


def login2(request, user):
    return render(request, 'users/login.html')


@login_required
def profile(request):

    # If the user submits new information to the update profile form this conditional will be true
    if request.method == 'POST' and 'form_submit' in request.POST:
        # fill out form according to the POST information
        update_prof_form = ProfileUpdateForm(request.POST, instance=request.user.profile)
        if update_prof_form.is_valid():
            # if the form information is valid save the information to the profile model in the sqlite database
            update_prof_form.save()
            messages.success(request, "Successfully updated profile data!", extra_tags='success')
            return redirect('profile')
    else:
        # if there is not a post request fill out the fields of the form with the logged in user's information
        update_prof_form = ProfileUpdateForm(instance=request.user.profile)


    # retrieve data in profile
    data = Profile.objects.filter(user = request.user)
    calories = carbs = fats = protein = goalWeight = currWeight = activity = starting_weight = {}
    for e in data:
        calories = e.daily_cal_in
        carbs = e.daily_carbs
        fats = e.daily_fat
        protein = e.daily_protein
        activity = e.activity_level
        weight = e.weight
        goalWeight = e.goal_weight_change

    #create graph for weight
    weightList = []
    dateList = []
    lbsList = []

    #Get the weight records for the current user sorted by the date
    weights = WeightRecord.objects.filter(user=request.user).order_by('date')

    #add the fields of the weight records to the 3 lists created above
    for e in weights:
        weightList.append(e)
        lbsList.append(e.lbs)
        dateList.append(e.date.strftime("%m-%d"))
    matplotlib.use('Agg')

    #style for the plot
    plt.style.use('seaborn')
    #plot the dates on the x axis and the
    plt.plot(dateList, lbsList, marker='*', markersize=5)


    for i in range(0, len(lbsList)):
        plt.annotate(lbsList[i], (dateList[i], lbsList[i]))
    plt.title('Weight History')
    plt.xlabel('Date')
    plt.ylabel('Weight (lbs)')

    weightFig = plt.gcf()
    weightBuf = io.BytesIO()
    weightFig.savefig(weightBuf, format='png')
    weightBuf.seek(0)
    string = base64.b64encode(weightBuf.read())
    weightGraph = urllib.parse.quote(string)
    plt.close()

    #create graph for lifts
    exerciseNames = []
    exercises = LiftRecord.objects.filter(user=request.user).order_by('-name')
    for e in exercises:
        if not e.name.lower().title() in exerciseNames and e.weight and e.reps:
           exerciseNames.append(e.name.lower().title())
    chosenName = ""
    if request.method == 'POST' and 'option_submit' in request.POST:
        if request.POST.get('exercise', False):
            chosenName = request.POST['exercise']
    

    chosenList = []
    date2List = []
    exercisesFiltered = LiftRecord.objects.filter(user=request.user).order_by('-date')
    for e in exercisesFiltered:
        if e.name.lower().title() == chosenName:
            chosenList.append(e.one_rep_max_equiv)
            date2List.append(e.date)
    matplotlib.use('Agg')
    plt.style.use('seaborn')
    plt.plot(date2List, chosenList, marker='D', markersize=5)
    for i in range(len(chosenList)):
        plt.annotate(chosenList[i], (date2List[i], chosenList[i]), ha="center")
    plt.title(chosenName.title() + ' Record')
    plt.xlabel('Date')
    plt.ylabel('Weight (lbs)')
    strengthFig = plt.gcf()
    strengthBuf = io.BytesIO()
    strengthFig.savefig(strengthBuf, format='png')
    strengthBuf.seek(0)
    string = base64.b64encode(strengthBuf.read())
    strengthGraph = urllib.parse.quote(string)
    plt.close()

    #create pie chart for daily macros
    foodDates = []
    foods = Food.objects.filter(user=request.user).order_by('-date')
    for e in foods:
        if not e.date in foodDates:
           foodDates.append(e.date)
    chosenDate = ""
    titleDate = ""
    if request.method == 'POST' and 'date_submit' in request.POST:
        if request.POST.get('date', False):
            chosenDate = request.POST['date']
            titleDate = chosenDate
            chosenDate = chosenDate.replace(".", "")
            chosenDate = datetime.datetime.strptime(str(parse(chosenDate)), '%Y-%m-%d %H:%M:%S').strftime("%Y-%m-%d")

    percentages = [0,0,0]
    totalCal = 0
    macroLabels = ['Carbohydrates', 'Fats', 'Protein']
    matplotlib.use('Agg')
    plt.style.use('seaborn')
    if chosenDate != "":
        foodsFiltered = Food.objects.filter(user=request.user,date=chosenDate)
        for e in foodsFiltered:
           
            percentages[0] += e.carbs
            percentages[1] += e.fats
            percentages[2] += e.protein
            totalCal += e.calories
           
        plt.pie(percentages, labels=macroLabels, autopct=lambda pct: pie_text_func(pct, percentages), shadow=True, startangle=90)

    totalCalStr = ""
    if titleDate != "":
        totalCalStr = "Total Calories: " + str(totalCal)
    plt.title("Macro Distribution " + str(titleDate) + "\n" + totalCalStr)

    #saves the plot as a png to display on html
    macroFig = plt.gcf()
    macroBuf = io.BytesIO()
    macroFig.savefig(macroBuf, format='png')
    macroBuf.seek(0)
    string = base64.b64encode(macroBuf.read())
    macroGraph = urllib.parse.quote(string)
    plt.close()

    daily_activity_desc = ["""Very light - Seated and standing activities, office work, driving, cooking; 
                           no vigorous activity
                           """,
                           """
                           Low active - In addition to the activities of a sedentary lifestyle, 30 minutes of moderate 
                           activity equivalent of walking 2 miles in 30 minutes; most office workers with additional 
                           planned exercise routines
                           """,
                           """
                           Active - In addition to the activities of a low active lifestyle, an additional 3 hours of 
                           activity such as bicycle 10-12 miles an hour, walk 4.5 miles an hour
                           """,
                           """
                           Heavy - Planned vigorous activities, physical labor, full-time athletes, hard-labor 
                           professions such as steel or road workers
                           """]
    if Profile.objects.filter(user=request.user).first().activity_level<1.4:
        daily_act = daily_activity_desc[0]
    elif Profile.objects.filter(user=request.user).first().activity_level<1.7:
        daily_act = daily_activity_desc[1]
    elif Profile.objects.filter(user=request.user).first().activity_level<1.8:
        daily_act = daily_activity_desc[2]
    else:
        daily_act = daily_activity_desc[3]
    if len(weightList) != 0:
        currWeight = weightList[0].lbs

    context = {
        'username': request.user.username,
        'loggedIn': False,
        'daily_act_info':daily_act,
        'update_prof_form': update_prof_form,
        'calories' : calories,
        'carbs' : carbs,
        'fats' : fats,
        'protein' : protein,
        'activity' : activity,
        'weight' : weight,
        'goalWeight' : goalWeight,
        'currWeight' : currWeight,
        'weightGraph': weightGraph,
        'exerciseNames' : exerciseNames,
        'strengthGraph' : strengthGraph,
        'foodDates' : foodDates,
        'macroGraph' : macroGraph,
    }
    if request.user.is_authenticated:
        context['loggedIn'] = True
    return render(request, 'users/profile.html', context)


def pie_text_func(pct, allvals):
    abso = int(pct/100.*np.sum(allvals))
    return "{:.1f}%\n({:d} g)".format(pct, abso)


@login_required
def weight(request):
    weightrecord = WeightRecord(user=request.user)
    if request.method == 'POST' and 'delete_but' in request.POST:
        deleted = WeightRecord.objects.filter(user=request.user, pk=request.POST['pk']).first()
        WeightRecord.objects.filter(user=request.user, pk=request.POST['pk']).delete()
        messages.success(request, "Successfully deleted weight!", extra_tags='success')

    if request.method == 'POST' and 'weight_graph' in request.POST:
        return redirect('profile')

    if request.method == 'POST' and 'form_submit' in request.POST:
        saveForm = True
        lbForm = WeightForm(request.POST, instance = weightrecord)
        if lbForm.is_valid():
            if lbForm.cleaned_data['lbs'] < 0:
                messages.error(request, "Please enter a valid weight.", extra_tags='danger')
                saveForm = False
            else:
                messages.success(request, "Successfully logged weight!", extra_tags='success')
            if saveForm:
                lbForm.save()
        else:
            messages.error(request, "Please re-enter valid information.", extra_tags='danger')
    form = WeightForm()
    data = WeightRecord.objects.filter(user=request.user).order_by('-date')
    size = len(data)
    stats = Profile.objects.filter(user=request.user)[0]
    goal = stats.goal_weight_change

    listG = []

    for e in data:
        listG.append((e.date, e.lbs, e))
    context = {
        'form' : form,
        'weights' : data,
        'size': size,
        'goal': goal,
        'listG': listG,
    }
    return render(request, 'users/weight.html', context)
  
@login_required
def macros(request):
    global MEALNAME
    foodName = ""
    foodDate = ""
    display = False

    if request.method == 'POST' and 'delete_but' in request.POST:
        deleted = Food.objects.filter(user = request.user, pk=request.POST['pk']).first()
        Food.objects.filter(user = request.user, pk=request.POST['pk']).delete()
        messages.success(request, "Successfully deleted food!", extra_tags='success')
    
    elif request.method == 'POST' and 'macro_distrib' in request.POST:
        return redirect('profile')

    if request.method == 'POST' and 'form2_submit' in request.POST:
        display = True
        singleFood = SingleFood(request.POST)
        if singleFood.is_valid():
            foodName = singleFood.cleaned_data['foodName'].capitalize()
            foodDate = singleFood.cleaned_data['date']
        else:
            messages.error(request, "Please re-enter valid information.", extra_tags='danger')        

        # URL = "https://www.acefitness.org/education-and-resources/lifestyle/exercise-library/body-part/abs/"
        r = requests.get("https://www.myfitnesspal.com/food/search?page=1&search="+str(foodName)) 

        soup = BeautifulSoup(r.content, 'html5lib') # If this line causes an error, run 'pip install html5lib' or install html5lib 
        if soup.find('div', attrs = {"class": "jss16"}) == None:
            messages.success(request, "Could not find food!", extra_tags='success')
            
        else:
            macroData = soup.find('div', attrs = {"class": "jss16"}).text
            servingSize = soup.find('div', attrs = {"class": "jss11"}).text
            servingSize = servingSize[servingSize.find(",")+2:]
            macroList = re.findall(r'[0-9]+', macroData) 
           
            food2 = Food(user=request.user)
            food2.name = foodName
            food2.calories = macroList[0]
            food2.carbs = macroList[1]
            food2.fats = macroList[2]
            food2.protein = macroList[3]
            food2.date = foodDate
            food2.save()
            messages.success(request, "Successfully added food!", extra_tags='success')
    #form2 = SingleFood()
    enter = MEALNAME
    form2 = SingleFood(initial={'foodName': enter})
            
    food = Food(user=request.user)
    if request.method == 'POST' and 'form_submit' in request.POST:
        foodForm = FoodForm(request.POST, instance = food)
        if foodForm.is_valid():
            food.name = foodForm.cleaned_data['name'].capitalize()
            stillValid = True
            if foodForm.cleaned_data['carbs'] < 0:
                stillValid = False
            if foodForm.cleaned_data['fats'] < 0:
                stillValid = False
            if foodForm.cleaned_data['protein'] < 0:
                stillValid = False
            if stillValid:
                messages.success(request, "Successfully logged food!", extra_tags='success')
                foodForm.save()
        else:
            messages.error(request, "Please re-enter valid information.", extra_tags='danger')
    form = FoodForm()
    data = Food.objects.filter(user = request.user).order_by('-date')
    dates = []
    size = len(data)

    for e in data:
        carbCal = 4 * e.carbs
        fatCal = 9 * e.fats
        proteinCal = 4 * e.protein
        e.calories = carbCal + fatCal + proteinCal
        e.save()
        if e.date not in dates:
            dates.append(e.date)
    context = {
        'form' : form,
        'form2': form2,
        'foods' : data,
        'display' : display,
        'dates': dates,
        'size': size,
    }
    MEALNAME = ""
    return render(request, 'users/macros.html', context)
    
@login_required
def exercises(request):
    lift_form_name = ""

    category = 'All'
    
    if request.method == 'POST' and 'delete_but' in request.POST:
        deleted = LiftRecord.objects.filter(user = request.user, pk=request.POST['pk']).first()
        LiftRecord.objects.filter(user = request.user, pk=request.POST['pk']).delete()
        messages.success(request, "Successfully deleted exercise!", extra_tags='success')
       

    if request.method == 'POST' and 'strength_graph' in request.POST:
        
        return redirect('profile')

    if request.method == 'POST':
        
        filter_form = ExerciseFilterForm(request.POST)
       
        if filter_form.is_valid():
            category = filter_form.cleaned_data['category']
            
            messages.success(request, "Successfully filtered exercises!", extra_tags='success')
        elif 'exercise_select' in request.POST:
            lift_form_name = request.POST['exercise_select']
            
            messages.success(request, "Successfully added exercise, log to complete!", extra_tags='success')
    #EXERCISES_GLOBAL = []
    if category =='All':
        threads = len(URLS)
        with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
            executor.map(scrap_url, URLS)

    else:
        EXERCISES_GLOBAL.clear()
        correct_index = 0
        for index, url in enumerate(URLS):
            for key in url:
                if key == category:
                    correct_index = index

        r = requests.get(URLS[correct_index][category])
        soup = BeautifulSoup(r.content, 'html5lib')  # If this line causes an error, run 'pip install html5lib' or install html5lib
        table = soup.find('div', attrs={'id': 'exerciseLibrary'})
        for row in table.findAll('div', attrs={"class": "exercise-card-grid__cell"}):
            exercise = {}
            exercise['category'] = category
            # exercise = {}
            exercise['name'] = row.find('div', attrs={"class": "exercise-card__body"}).header.h2.text
            # exercise['name'] = row.header.h2.text

            exercise['equipment'] = row.find('div', attrs={
                "class": "exercise-info__term exercise-info__term--equipment"}).dd.text
            exercise['img'] = row.find('div', attrs={"class": "exercise-card__image"})['style'].split("'")[1]
            exercise['description_link'] = 'https://www.acefitness.org/' + row.a['href']

            EXERCISES_GLOBAL.append(exercise)
    filter_form = ExerciseFilterForm(initial={'category': category})

    liftrecord = LiftRecord(user=request.user)
    if request.method == 'POST' and 'form_submit' in request.POST:
        liftForm = LiftForm(request.POST, instance=liftrecord)
        if liftForm.is_valid():
            stillValid = True
            skip = True
            if not str(liftForm.cleaned_data['weight']).isdigit() or not str(liftForm.cleaned_data['sets']).isdigit() or not str(liftForm.cleaned_data['reps']).isdigit():
                #liftForm.save()
                skip = False
            if skip and liftForm.cleaned_data['weight'] < 0 :
                messages.error(request, "Please enter a valid number for weight.", extra_tags='danger')
                stillValid = False
            if skip and liftForm.cleaned_data['sets'] < 0 :
                messages.error(request, "Please enter a valid number for sets.", extra_tags='danger')
                stillValid = False
            if skip and liftForm.cleaned_data['reps'] < 0 :
                messages.error(request, "Please enter a valid number for reps.", extra_tags='danger')
                stillValid = False
            if stillValid:
                liftForm.save()
                messages.success(request, "Successfully logged exercise!", extra_tags='success')
                
                liftForm.save()
        else:
            messages.error(request, "Please re-enter valid information.", extra_tags='danger')
    form = LiftForm(initial={'name': lift_form_name})
    # filter_form = ExerciseFilterForm()
    data = LiftRecord.objects.filter(user=request.user).order_by('-date')
    size = len(data)
   
    context = {
        'exercises': EXERCISES_GLOBAL,
        'title': 'Exercises',
        'form': form,
        'filter': filter_form,
        'lifts': data,
        'size' : size
    }

    return render(request, 'users/exercises.html', context)


def scrap_url(url):
    for key in url:
        r = requests.get(url[key])

        soup = BeautifulSoup(r.content, 'html5lib')  # If this line causes an error, run 'pip install html5lib' or install html5lib

        table = soup.find('div', attrs = {'id':'exerciseLibrary'})
       
        for row in table.findAll('div', attrs = {"class" : "exercise-card-grid__cell"}):
           
            exercise = {}
            exercise['category'] = key
            # exercise = {}
            exercise['name'] = row.find('div', attrs={"class": "exercise-card__body"}).header.h2.text
            # exercise['name'] = row.header.h2.text

            exercise['equipment'] = row.find('div', attrs={
                "class": "exercise-info__term exercise-info__term--equipment"}).dd.text
            exercise['img'] = row.find('div', attrs={"class": "exercise-card__image"})['style'].split("'")[1]
            exercise['description_link'] = 'https://www.acefitness.org/' + row.a['href']
            EXERCISES_GLOBAL.append(exercise)

@login_required
def meals(request):
    global MEALNAME

    category = 'All'
    if request.method == 'POST' and 'log_submit' in request.POST:
        
        MEALNAME = request.POST['log_submit']
        return redirect('macros')

    if request.method == 'POST' and 'filter_submit' in request.POST:
        
        filter_form = MealFilterForm(request.POST)
        if filter_form.is_valid():
            category = filter_form.cleaned_data['category']
            

    if category == 'All':
        URL = 'https://www.skinnytaste.com/recipes/' + category + '/'
    else:
        URL = 'https://www.skinnytaste.com/recipes/' + category + '/'

    r = requests.get(URL)

    soup = BeautifulSoup(r.text, 'lxml')
    recipe_list = []
    recipe_dict = {}

    for tag in soup.find_all('div', class_="archive-post"):
        recipe_dict['link'] = tag.find('a')['href']
        recipe_dict['title'] = tag.find('a')['title']
        recipe_dict['img'] = tag.find('img')['src']
        recipe_list.append(recipe_dict)
        recipe_dict = {}

    count = 1
    while count < 5:
        URL = 'https://www.skinnytaste.com/recipes/page/' + str(count) + '/'
        r = requests.get(URL)
        soup = BeautifulSoup(r.text, 'lxml')
        count += 1
        for tag in soup.find_all('div', class_="archive-post"):
            recipe_dict['link'] = tag.find('a')['href']
            recipe_dict['title'] = tag.find('a')['title']
            recipe_dict['img'] = tag.find('img')['src']
            recipe_list.append(recipe_dict)
            recipe_dict = {}

    filter_form = MealFilterForm(initial={'category': category})
    context = {
        'meals': recipe_list,
        'title': 'Meals',
        'filter': filter_form,
    }

    return render(request, 'users/meals.html', context)
