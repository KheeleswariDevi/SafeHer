
from django.db import models
from django.contrib.auth.models import User

class HazardReport(models.Model):
    street_name = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    description = models.TextField()
    reported_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    latitude = models.FloatField(null=True, blank=True)  # Add latitude field
    longitude = models.FloatField(null=True, blank=True)  # Add longitude field

    def __str__(self):
        return f"Report at {self.street_name}, {self.city}, {self.country}"


class HazardComment(models.Model):
    report = models.ForeignKey(HazardReport, on_delete=models.CASCADE, related_name="comments")
    comment_text = models.TextField()
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Link to the User model
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    favorite_locations = models.TextField(null=True, blank=True)
    
    # Emergency contacts fields (add more if needed)
    emergency_contact_name_1 = models.CharField(max_length=100, null=True, blank=True)
    emergency_contact_phone_1 = models.CharField(max_length=15, null=True, blank=True)
    emergency_contact_priority_1 = models.CharField(max_length=10, null=True, blank=True)
    
    emergency_contact_name_2 = models.CharField(max_length=100, null=True, blank=True)
    emergency_contact_phone_2 = models.CharField(max_length=15, null=True, blank=True)
    emergency_contact_priority_2 = models.CharField(max_length=10, null=True, blank=True)
    
    emergency_contact_name_3 = models.CharField(max_length=100, null=True, blank=True)
    emergency_contact_phone_3 = models.CharField(max_length=15, null=True, blank=True)
    emergency_contact_priority_3 = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'


from django.db import models


class ReportedHazardArea(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return self.name



class SubscriptionPlan(models.Model):

    PLAN_TYPES = [
        ('basic', 'Basic Plan - Monthly'),
        ('premium', 'Premium Plan - Monthly/Yearly'),
        ('enterprise', 'Enterprise Plan - Custom'),
    ]

    name = models.CharField(max_length=50, choices=PLAN_TYPES)
    description = models.TextField()
    monthly_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    yearly_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.name


class PromoCode(models.Model):

    code = models.CharField(max_length=50, unique=True)
    discount_percentage = models.FloatField()
    valid_till = models.DateField()

    def is_valid(self):

        from datetime import date
        return date.today() <= self.valid_till


class Payment(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=50)  # Example: Credit Card, PayPal, etc.
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    subscription_start = models.DateField(auto_now_add=True)
    subscription_end = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.user} - {self.plan.name}"
