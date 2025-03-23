from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views 

urlpatterns = [
    path('', views.login_view, name='login'),
    path("login-reg/",  views.register_view, name="login-reg"), 
    path('home', views.home, name='home'),
    path('sip-calculator/', views.sip_calculator, name='sip_calculator'),
    path('emi-calculator/', views.emi_calculator, name='emi_calculator'),
    path('fin-edu/', views.fin_edu_home, name='fin-edu'),
    
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('register/', views.register, name='register'),
    path('user-profile/', views.profile, name='user-profile'),
    path('ai-insights/', views.create_financial_goal, name='create_financial_goal'),
    path("contact/", views.contact_view, name="contact"),
    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

