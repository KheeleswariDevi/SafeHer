from django.shortcuts import render, redirect
from django.contrib.auth import login, logout 
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .forms import *
from django.contrib.auth.decorators import login_required
from .models import *
from django.contrib import messages
from django.http import HttpResponse
from django.core.mail import send_mail




def index(request):
     return render(request, 'index.html')


def tracking(request):
    return render(request, 'tracking.html') 


def chat(request):
    return render(request, 'chat.html')


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  
            return redirect('index')  
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index') 
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('index')  


def hazardous_areas_view(request):
    reports = HazardReport.objects.all()
    reports_data = []

    for report in reports:
        address = f"{report.street_name}, {report.city}, {report.country}"
        reports_data.append({
            "location_name": address,
            "description": report.description,
            "reported_by": report.reported_by.username if report.reported_by else "Anonymous",
            "timestamp": report.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            "latitude": report.latitude,
            "longitude": report.longitude,
        })

    return render(request, "tracking.html", {"reports_data": list(reports_data)})


@login_required
def add_hazard_report(request):
    if request.method == "POST":
        form = HazardReportForm(request.POST)
        if form.is_valid():
            hazard_report = form.save(commit=False)
            hazard_report.reported_by = request.user
            hazard_report.save()
            messages.success(request, "Hazard report submitted successfully.")
            return redirect('hazardous_areas_view')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = HazardReportForm()
    return render(request, 'add_hazard_report.html', {'form': form})

from django.shortcuts import render, redirect
from .forms import ReportHazardForm


def report_hazard(request):
    if request.method == 'POST':
        form = ReportHazardForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('hazard_report')
    else:
        form = ReportHazardForm()

    # Pass initial latitude and longitude into context dynamically
    context = {
        'form': form,
    }

    return render(request, 'report_hazard.html', context)



@login_required
def view_profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)  
    return render(request, 'view_profile.html', {'profile': profile})




@login_required
def edit_profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('view_profile')  
        else:
            messages.error(request, 'There was an issue updating your profile. Please try again.')
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'edit_profile.html', {'form': form})



def privacy_policy(request):
    return render(request, 'privacy_policy.html')

def terms_of_service(request):
    return render(request, 'terms_of_service.html')


def incognito_mode(request):
    return render(request, 'incognito_mode.html')


def contact_us(request):
    form = ContactForm()
    return render(request, 'contact_us.html', {'form': form})

def submit_contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            # Send email
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            
            send_mail(
                subject=f"New Contact Form Submission from {name}",
                message=message,
                from_email=email,
                recipient_list=['support@safeher.com'],
            )

            # Redirect to the thank_you page after the email is sent
            return redirect('thank_you')  # Redirect to the thank_you URL

    # If the form is not valid, render the contact page again
    form = ContactForm()
    return render(request, 'contact_us.html', {'form': form})

def thank_you(request):
    return render(request, 'thank_you.html')


from django.shortcuts import render, redirect
from .models import SubscriptionPlan, PromoCode, Payment
from .forms import PaymentForm


def payment_view(request):

    plans = SubscriptionPlan.objects.all()
    promo_valid = None
    if request.method == "POST":
        form = PaymentForm(request.POST)
        if form.is_valid():
            plan_id = form.cleaned_data['plan']
            payment_method = form.cleaned_data['payment_method']
            promo_code = form.cleaned_data['promo_code']
            plan = SubscriptionPlan.objects.get(id=plan_id)
            discount = 0

            if promo_code:
                try:
                    promo = PromoCode.objects.get(code=promo_code)
                    if promo.is_valid():
                        discount = (promo.discount_percentage / 100) * plan.monthly_price
                        promo_valid = True
                    else:
                        promo_valid = False
                except PromoCode.DoesNotExist:
                    promo_valid = False

            final_amount = plan.monthly_price - discount

            Payment.objects.create(
                user=request.user,
                plan=plan,
                payment_method=payment_method,
                amount_paid=final_amount
            )

            return render(request, 'payment_success.html', {'amount': final_amount})

    else:
        form = PaymentForm()

    return render(request, 'payment.html', {'plans': plans, 'form': form, 'promo_valid': promo_valid})


