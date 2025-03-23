from django import forms
from .models import SIP, Loan,Lesson,UserProfile, User, FinancialGoal, ContactMessage
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

class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))

class RegisterForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["username", "email", "password"]

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            self.add_error("confirm_password", "Passwords do not match.")

        return cleaned_data

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'message']

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if not email.endswith("@gmail.com"):  # Example validation
            raise forms.ValidationError("Only Gmail addresses are allowed.")
        return email