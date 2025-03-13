from django.shortcuts import render, redirect,get_object_or_404
from django.http import HttpResponseBadRequest
from .models import SIP,Loan,Lesson,UserProfile,User, FinancialGoal
from .forms import SIPForm, LoanForm,LessonForm,UserProfileForm, FinancialGoalForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from datetime import date
from django.http import JsonResponse

def home(request):
    return render(request, 'finance/home.html')


# SIP Calculation View
def sip_calculator(request):
    if request.method == 'POST':
        form = SIPForm(request.POST)
        if form.is_valid():
            # Get cleaned data from the form
            principal_amount = form.cleaned_data['principal_amount']
            rate_of_interest = form.cleaned_data['rate_of_interest']
            time_period = form.cleaned_data['time_period']
            monthly_sip = form.cleaned_data['monthly_sip']

            # Create an SIP instance for calculation (no need to save to the database)
            sip = SIP(principal_amount=principal_amount, rate_of_interest=rate_of_interest, 
                      time_period=time_period, monthly_sip=monthly_sip)

            # Calculate maturity amount
            maturity_amount = sip.calculate_maturity()

            # Return the result to the template
            return render(request, 'finance/sip_result.html', {'maturity_amount': maturity_amount})

    else:
        form = SIPForm()

    return render(request, 'finance/sip_calculator.html', {'form': form})


# EMI Calculation View
def emi_calculator(request):
    emi = None  # Initialize EMI variable
    
    if request.method == 'POST':
        try:
            loan_amount = float(request.POST.get('loan_amount'))
            interest_rate = float(request.POST.get('interest_rate'))
            tenure = int(request.POST.get('tenure'))

            # EMI formula
            interest_rate_monthly = interest_rate / 12 / 100  # Annual interest rate converted to monthly
            tenure_months = tenure * 12

            if interest_rate_monthly == 0:  # If interest rate is 0, use a simple formula
                emi = loan_amount / tenure_months
            else:
                emi = loan_amount * interest_rate_monthly * (1 + interest_rate_monthly) ** tenure_months / ((1 + interest_rate_monthly) ** tenure_months - 1)
            
            emi = round(emi, 2)  # Round to 2 decimal places

        except (ValueError, KeyError) as e:
            # If any errors happen with form data, log the error and return a bad request
            print(f"Error occurred: {e}")
            return HttpResponseBadRequest("Invalid input data. Please check your input values.")

    return render(request, 'finance/emi-calculator.html', {'emi': emi})


# financial_education/views.py

def fin_edu_home(request):
    form = LessonForm(request.GET)  # Use GET method to capture the search keyword from the URL
    lessons = Lesson.objects.all()  # Start with all lessons
    error_message = None

    keyword = request.GET.get('keyword', '').strip()

    # If there is a search term (and not empty), filter by title and content
    if keyword:
        lessons = lessons.filter(title__icontains=keyword) | lessons.filter(content__icontains=keyword)
    else:
        # If the keyword is empty, show an error message
        error_message = "Please enter a search term."

    return render(request, 'finance/financial_edu_page.html', {
        'form': form,
        'lessons': lessons,
        'error_message': error_message
    })

@login_required
def profile(request):
    # Retrieve or create the user's profile
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    return render(request, 'accounts/profile.html', {'profile': profile})

@login_required
def register(request):
    # Retrieve or create the user's profile
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if profile_form.is_valid():
            profile_form.save()  # Save the profile data
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('profile')  # Redirect back to the profile page
        else:
            messages.error(request, 'Please correct the errors in the form.')
    else:
        profile_form = UserProfileForm(instance=profile)  # Prepopulate the form with existing profile data

    return render(request, 'accounts/register.html', {'form': profile_form})

@login_required
def create_financial_goal(request):
    suggestions = []  # List to store suggestions
    completed = 0
    remaining = 0

    if request.method == 'POST':
        form = FinancialGoalForm(request.POST)
        
        if form.is_valid():
            # Save the goal
            financial_goal = form.save(commit=False)
            if not financial_goal.amount:
                financial_goal.amount = 0  # Default value if 'amount' is not provided

            # Add suggestion based on risk appetite
            if financial_goal.risk_appetite:
                if financial_goal.risk_appetite == 'low':
                    suggestions.append("Consider saving at a slower but safer pace. Try low-risk investments.")
                elif financial_goal.risk_appetite == 'medium':
                    suggestions.append("Consider diversifying your investments to balance growth and safety.")
                elif financial_goal.risk_appetite == 'high':
                    suggestions.append("You're taking high risks! Consider more aggressive investments for higher potential returns.")

            # Add suggestion based on target date and amount
            if financial_goal.target_amount:
                if financial_goal.target_amount > 10000:
                    suggestions.append("Your target amount is quite high! Make sure to track your progress regularly.")
                if financial_goal.target_date:
                    target_date = financial_goal.target_date
                    today = date.today()
                    months_left = (target_date.year - today.year) * 12 + target_date.month - today.month
                    if months_left < 6:
                        suggestions.append("You're running out of time to reach your target! Consider increasing your savings rate.")
                    elif months_left > 36:
                        suggestions.append("You have plenty of time to reach your goal! Consider a lower monthly contribution.")

            # Save the goal to the database
            financial_goal.user = request.user
            financial_goal.save()

            # Get the goal's progress data
            completed = financial_goal.amount
            remaining = financial_goal.target_amount - completed

            # Check if the request is AJAX
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({
                    'completed': completed,
                    'remaining': remaining,
                    'suggestions': suggestions
                })

            # Otherwise, render the response
            return render(request, 'finance/ai-insight.html', {
                'form': form,
                'suggestions': suggestions,
                'completed': completed,
                'remaining': remaining
            })

    else:
        form = FinancialGoalForm()

    return render(request, 'finance/ai-insight.html', {
        'form': form,
        'suggestions': suggestions,
        'completed': completed,
        'remaining': remaining
    })