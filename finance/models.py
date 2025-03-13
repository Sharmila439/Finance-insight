from django.db import models
from django.contrib.auth.models import User
from embed_video.fields import EmbedVideoField
from django.utils import timezone

# Create your models here.
    
# SIP Calculator Model (Systematic Investment Plan)

class SIP(models.Model):
    principal_amount = models.FloatField()  # Initial investment (P)
    rate_of_interest = models.FloatField()  # Annual interest rate (R)
    time_period = models.IntegerField()  # Time period in years (T)
    monthly_sip = models.FloatField()  # Monthly SIP contribution (S)

    def __str__(self):
        return f"SIP Plan: {self.principal_amount} at {self.rate_of_interest}% interest"

    def calculate_maturity(self):
        P = self.principal_amount  # Principal amount
        R = self.rate_of_interest  # Interest rate (annual percentage)
        T = self.time_period  # Time period (years)
        S = self.monthly_sip  # Monthly SIP contribution

        # Monthly interest rate
        rate = R / 100 / 12
        n = T * 12  # Total number of months

        # SIP maturity formula (simplified)
        maturity_amount = S * (((1 + rate) ** n - 1) / rate) * (1 + rate) + P * (1 + R / 100) ** T

        return round(maturity_amount, 2)




# EMI Calculator Model (Loan)
class Loan(models.Model):
    loan_amount = models.DecimalField(max_digits=10, decimal_places=2)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    tenure = models.PositiveIntegerField()

    def calculate_emi(self):
        p = self.loan_amount
        r = self.interest_rate / 100 / 12
        n = self.tenure * 12
        emi = (p * r * (1 + r) ** n) / ((1 + r) ** n - 1)
        return emi

    
#financial eduaction  
class Lesson(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()  # Description or summary of the lesson
    published_date = models.DateTimeField(auto_now_add=True)
    video = EmbedVideoField() 

    def __str__(self):
        return self.title
    
#user profile  
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pics/', default='default.jpg', blank=True)
    income = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    savings_goals = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    expenses = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    social_links = models.JSONField(default=dict, blank=True)  # Store social links as a JSON dictionary
    last_updated = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.user.username} Profile'

    def get_profile_picture(self):
        if not self.profile_picture:
            return 'data:image/jpeg;base64,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'
        return self.profile_picture.url
    
#ai-insight
class FinancialGoal(models.Model):
    goal_name = models.CharField(max_length=255)
    target_amount = models.DecimalField(max_digits=10, decimal_places=2)
    target_date = models.DateField()
    email = models.EmailField()
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # Default value
    name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    risk_appetite = models.CharField(
        max_length=50, 
        choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')], 
        null=True, 
        blank=True
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    GOAL_TYPE_CHOICES = [
        ('saving', 'Saving'),
        ('investment', 'Investment'),
        ('debt_reduction', 'Debt Reduction'),
        ('retirement', 'Retirement'),
    ]
    goal_type = models.CharField(
        max_length=50,
        choices=GOAL_TYPE_CHOICES,
        null=True,
        blank=True
    )

    def __str__(self):
        return f'{self.goal_name} - {self.target_amount}'
