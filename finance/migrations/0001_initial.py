# Generated by Django 5.1.6 on 2025-03-04 15:34

import django.db.models.deletion
import django.utils.timezone
import embed_video.fields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('content', models.TextField()),
                ('published_date', models.DateTimeField(auto_now_add=True)),
                ('video', embed_video.fields.EmbedVideoField()),
            ],
        ),
        migrations.CreateModel(
            name='Loan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('loan_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('interest_rate', models.DecimalField(decimal_places=2, max_digits=5)),
                ('tenure', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='SIP',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('principal_amount', models.FloatField()),
                ('rate_of_interest', models.FloatField()),
                ('time_period', models.IntegerField()),
                ('monthly_sip', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='FinancialGoal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('name', models.CharField(max_length=100)),
                ('date_of_birth', models.DateField(blank=True, null=True)),
                ('risk_appetite', models.CharField(blank=True, choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')], max_length=50, null=True)),
                ('goal_name', models.CharField(max_length=100)),
                ('goal_type', models.CharField(max_length=50)),
                ('target_amount', models.DecimalField(decimal_places=2, max_digits=15)),
                ('target_date', models.DateField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile_picture', models.ImageField(blank=True, default='default.jpg', upload_to='profile_pics/')),
                ('income', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('savings_goals', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('expenses', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('address', models.CharField(blank=True, max_length=255, null=True)),
                ('date_of_birth', models.DateField(blank=True, null=True)),
                ('social_links', models.JSONField(blank=True, default=dict)),
                ('last_updated', models.DateTimeField(default=django.utils.timezone.now)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
