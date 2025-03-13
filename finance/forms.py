from django import forms
from .models import SIP, Loan,Lesson,UserProfile, User, FinancialGoal
from django.contrib.auth.models import User

class SIPForm(forms.ModelForm):
    class Meta:
        model = SIP
        fields = ['principal_amount', 'rate_of_interest', 'time_period', 'monthly_sip']  # Correct field names


class LoanForm(forms.ModelForm):
    class Meta:
        model = Loan
        fields = ['loan_amount', 'interest_rate', 'tenure']

class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['title', 'content', 'video']  # Include the video field
        keyword = forms.CharField(label='Search', max_length=100, required=False)

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_picture', 'income', 'savings_goals', 'expenses', 'address', 'date_of_birth', 'social_links']
        
        widgets = {
            'social_links': forms.Textarea(attrs={'placeholder': 'Add your social links here in JSON format (e.g., {"facebook": "link"})'}),
            'date_of_birth': forms.DateInput(attrs={'type': 'date'})
        }



class FinancialGoalForm(forms.ModelForm):
    class Meta:
        model = FinancialGoal
        fields = ['name','email','date_of_birth','amount','goal_name', 'goal_type', 'target_amount', 'target_date', 'risk_appetite']
        