import datetime
from django.contrib import messages
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as dj_login
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Sum
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.forms import UserChangeForm
from .forms import UserProfileForm
from .forms import AddExpenseForm
from django.contrib.auth.decorators import login_required
from django.db.models import F

from .models import AddExpense_info, UserProfile


def home(request):
    """returns landing page
    if request.session.has_key('is_logged'):
        return redirect('budgetpad/dashboard')"""
    return render(request, 'home.html')


def handleSignup(request):
    """handles the backend of signup form. Uname, fname, lname, email,
    pass1, pass2, income, savings and profession will store the 
    information of the form in these variables."""
    if request.method == 'POST':
        # gets the post parameters
        uname = request.POST.get("uname")
        email = request.POST.get("email")
        pass1 = request.POST.get("pass1")
        pass2 = request.POST["pass2"]

        # check if passwords match
        if pass1 != pass2:
            messages.error(
                request, " Password do not match, Try again!!!")
            return redirect('/register')

        # username should not exceed 12 characters
        if len(uname) > 12:
            messages.error(
                request, " Username must be max 12 characters, Please try again")
            return redirect("/register")

        # check if username already taken
        try:
            if User.objects.get(username=uname):
                messages.error(
                    request, "Username already taken, Try something else!!!")
                return redirect("/signup")
        except User.DoesNotExist:
            user = User.objects.create_user(uname, email, pass1)
            messages.success(request, "Account created successfully")
            return redirect('/login')

        # create the user
        user = User.objects.create_user(
            username=uname, email=email, password=pass1)
        user.save()

        # Create a UserProfile instance and associate it with the User
        user_profile = UserProfile.objects.create(user=user)

        # Set the additional fields on the UserProfile instance
        user_profile.profession = request.POST['profession']
        user_profile.income = request.POST['income']
        user_profile.save()

        # Response message
        messages.success(
            request, " Your account has been successfully created")
        return redirect('login')

    return render(request, 'budgetpad/signup.html')


def handleLogin(request):
    """If the info entered by the user is correct, redirected to the dashboard."""
    if request.method == 'POST':
        # get the post parameters
        uname = request.POST["loginuname"]
        email = request.POST["loginemail"]
        pass1 = request.POST["loginpass1"]
        user = authenticate(request, username=uname, email=email,
                            password=pass1)
        if user is not None:
            # login user and create a session
            dj_login(request, user)
            request.session['is_logged'] = True
            user = request.user.id
            request.session["user_id"] = user
            messages.success(request, " Successfully logged in")
            return redirect('dashboard')
        else:
            # Invalid credentials to display error message
            messages.error(
                request, " Invalid email or password, Please try again")
            return redirect("/login")
    else:
        return render(request, 'budgetpad/login.html')


def handleLogout(request):
    """Function handles the logout backend logic"""
    del request.session['is_logged']
    del request.session["user_id"]
    logout(request)
    messages.success(request, " Successfully logged out")
    return redirect('home')


@login_required
def profile(request):
    """Redirects the user to the profile page"""
    """user_profile = request.user.userprofile
    return render(request,
                  'budgetpad/profile.html',
                  {"user_profile": user_profile})"""

    if request.session.has_key('is_logged'):
        return render(request,
                      'budgetpad/profile.html')
    return redirect('/home')


def profile_edit(request):
    """to page where user profile can be edited."""
    # if request.session_has_key('is_logged'):
    # add = User.objects.get(id=id)
    user = request.user
    form = UserProfileForm(instance=user.userprofile)
    return render(request,
                  'budgetpad/profile_update.html', {'form': form})


def profile_update(request):
    """performs the backend of the edit profile form."""
    # user = User.objects.get(id=id)
    user = request.user
    profile = user.userprofile

    if request.method == "POST":
        form = UserProfileForm(request.POST, instance=user)
        if form.is_valid():
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            profile.profession = form.cleaned_data['profession']
            profile.income = form.cleaned_data['income']
            # user.userprofile.profile_completed = True
            form.save()
            profile.profile_completed = True
            profile.save()
            return redirect('profile')
    else:
        form = UserProfileForm(instance=user)

    return redirect('profile_edit')


@login_required
def dashboard(request):
    """ returns the dashboard view for authenticated users """
    if request.session.has_key('is_logged'):
        # user_id = request.session["user_id"]
        user_profile = request.user.userprofile

    profile_completed = user_profile.profile_completed
    if profile_completed:
        # if request.session.has_key('is_logged') and profile is completed
        return render(request,
                      'budgetpad/dashboard.html',)
    else:
        # if profile is not completed
        return render(request, "budgetpad/profile_update.html")


def calculator(request):
    """redirects to calculator page"""
    return render(request, 'budgetpad/calculator.html')


def expenses(request):
    """redirects user to expenses page"""
    if request.session.has_key('is_logged'):
        user_id = request.session["user_id"]
        user = User.objects.get(id=user_id)

        # Default sorting by due date
        sort_by = request.GET.get('sort_by', 'due_date')
        if sort_by == 'category':
            expenses = AddExpense_info.objects.filter(
                user=user).order_by('category')
        else:
            expenses = AddExpense_info.objects.filter(
                user=user).order_by(F('due_date').asc(nulls_last=True))
        paginator = Paginator(expenses, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {
            'page_obj': page_obj,
            'sort_by': sort_by
        }
        return render(request, 'budgetpad/expenses.html', context)
    return redirect('dashboard')


def addExpense(request):
    """renders the add expenses and income."""
    if request.session.has_key('is_logged'):
        expenses = AddExpense_info.objects.filter(
            user=request.user).order_by('due_date')
        return render(request, 'budgetpad/add-expenses.html', {'expenses': expenses})
    return redirect('dashboard')

    """form = AddExpenseForm()
    return render(request, 'budgetpad/add-expenses.html', {'form': form})
    """


def addExpense_submission(request):
    """handles the submission of the expense form"""
    if request.session.has_key('is_logged'):
        if request.method == "POST":
            form = AddExpenseForm(request.POST)
            if form.is_valid():
                expense = form.save(commit=False)
                expense.user = request.user
                expense.save()

                # Automatically assign expense number
                expense.expense_number = AddExpense_info.objects.filter(
                    user=request.user).count()
                expense.save()
                return redirect('expenses')
        else:
            form = AddExpenseForm()
        return render(request,
                      'budgetpad/add-expenses.html', {'form': form})
    return redirect('dashboard')


def expense_edit(request, expense_id):
    """function to edit an expense"""
    if request.session.has_key('is_logged'):
        expense = get_object_or_404(
            AddExpense_info, id=expense_id, user=request.user)

        if request.method == 'POST':
            form = AddExpenseForm(request.POST, instance=expense)
            if form.is_valid():
                form.save()
                return redirect('expenses')
        else:
            form = AddExpenseForm(instance=expense)

        return render(request, 'budgetpad/expense_edit.html', {'form': form, 'expense': expense})
    return redirect('dashboard')


def expense_delete(request, expense_id):
    """deletes an expense"""
    if request.session.has_key('is_logged'):
        expense = get_object_or_404(
            AddExpense_info, id=expense_id, user=request.user)
        expense.delete()
        return redirect('expenses')
    return redirect('dashboard')


def addExpense_update(request, id):
    """saves the info of the form after it's been edited"""
    if request.session.has_key('is_logged'):
        if request.method == "POST":
            add = AddExpense_info.objects.get(id=id)
            add .add_expense = request.POST["add_expense"]
            add.amount = request.POST["amount"]
            add.due_date = request.POST["due_date"]
            add.category = request.POST["category"]
            add .save()
            return redirect("/dashboard")
    return redirect("/home")


def expense_month(request):
    """gets the data of the expenses of the current month."""
    todays_date = datetime.date.today()
    one_month_ago = todays_date-datetime.timedelta(days=30)
    user_id = request.session["user_id"]
    user1 = User.objects.get(id=user_id)
    addExpense = AddExpense_info.objects.filter(
        user=user1, Date__gte=one_month_ago, Date__lte=todays_date)
    finalrep = {}

    def get_Category(addExpense_info):
        """gets the category (expense/income) from the database"""
        # if addExpense_info.add_Expense=="Expense":
        return addExpense_info.Category
    Category_list = list(set(map(get_Category, addExpense)))

    def get_expense_category_amount(Category, add_expense):
        """fetches the amount from the database of the expense category"""
        amount = 0
        filtered_by_category = addExpense.filter(
            Category=Category, add_expense="Expense")
        for item in filtered_by_category:
            amount += item.amount
        return amount

    for x in addExpense:
        for y in Category_list:
            finalrep[y] = get_expense_category_amount(y, "Expense")

    return JsonResponse({'expense_category_data': finalrep}, safe=False)


def stats(request):
    """calculates the overall expenses made by user in a month."""
    if request.session.has_key('is_logged'):
        todays_date = datetime.date.today()
        one_month_ago = todays_date-datetime.timedelta(days=30)
        user_id = request.session["user_id"]
        user1 = User.objects.get(id=user_id)
        addExpense_info = AddExpense_info.objects.filter(
            user=user1, Date__gte=one_month_ago, Date__lte=todays_date)
        total_expense = 0  # initialize total expense variable
        for i in addExpense_info:
            if i.add_expense == 'Expense':
                total_expense += i.amount
        addExpense_info.sum = total_expense
        total_income = 0
        for i in addExpense_info:
            if i.add_expense == 'Income':
                total_income += i.amount
        return render(request, 'budgetpad/expenses-history.html', {'addExpense': addExpense_info})


def expense_week(request):
    """Overall expense by the week"""
    todays_date = datetime.date.today()
    one_week_ago = todays_date-datetime.timedelta(days=7)
    user_id = request.session["user_id"]
    user1 = User.objects.get(id=user_id)
    addExpense = AddExpense_info.objects.filter(
        user=user1, Date__gte=one_week_ago, Date__lte=todays_date)
    finalrep = {}

    def get_Category(addExpense_info):
        return addExpense_info.Category
    Category_list = list(set(map(get_Category, addExpense)))

    def get_expense_category_amount(Category, add_expense):
        amount = 0
        filtered_by_category = addExpense.filter(
            Category=Category, add_expense="Expense")
        for item in filtered_by_category:
            amount += item.amount
        return amount

    for x in addExpense:
        for y in Category_list:
            finalrep[y] = get_expense_category_amount(y, "Expense")

    return JsonResponse({'expense_category_data': finalrep}, safe=False)


def weekly(request):
    """Oerall expenses of a user."""
    if request.session.has_key('is_logged'):
        todays_date = datetime.date.today()
        one_week_ago = todays_date-datetime.timedelta(days=7)
        user_id = request.session["user_id"]
        user1 = User.objects.get(id=user_id)
        addExpense_info = AddExpense_info.objects.filter(
            user=user1, Date__gte=one_week_ago, Date__lte=todays_date)
        weeklyExpense = addExpense_info.aggregate(Sum('amount'))['amount__sum']
        weeklyIncome = addExpense_info.aggregate(Sum('amount'))['amount__sum']

    return render(request, 'home/weekly.html',
                  {'addExpense_info': addExpense_info})


def check(request):
    if request.method == 'POST':
        user_exists = User.objects.filter(email=request.POST['email'])
        messages.error(request, "Email not registered, TRY AGAIN!!!")
        return redirect("/reset_password")


def info_year(request):
    """gets the data of the expenses of the current year"""
    todays_date = datetime.date.today()
    one_week_ago = todays_date-datetime.timedelta(days=30*12)
    user_id = request.session["user_id"]
    user1 = User.objects.get(id=user_id)
    addExpense = AddExpense_info.objects.filter(
        user=user1, Date__gte=one_week_ago, Date__lte=todays_date)
    finalrep = {}

    def get_Category(addExpense_info):
        return addExpense_info.Category
    Category_list = list(set(map(get_Category, addExpense)))

    def get_expense_category_amount(Category, add_expense):
        amount = 0
        filtered_by_category = addExpense.filter(
            Category=Category, add_expense="Expense")
        for item in filtered_by_category:
            amount += item.amount
        return amount

    for x in addExpense:
        for y in Category_list:
            finalrep[y] = get_expense_category_amount(y, "Expense")

    return JsonResponse({'expense_category_data': finalrep}, safe=False)


def info(request):
    """about"""
    return render(request, 'budgetpad/about-us.html')
