from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import HazardReport, HazardComment, Profile

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    date_of_birth = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=True,
        label="Date of Birth"
    )
    address = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3}),
        required=True,
        label="Address"
    )
    emergency_contact_name_1 = forms.CharField(required=True, label="Emergency Contact Name")
    emergency_contact_phone_1 = forms.CharField(required=True, label="Emergency Contact Phone Number")
    emergency_contact_priority_1 = forms.CharField(required=True, label="Emergency Contact Priority Level 1")

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            Profile.objects.create(
                user=user,
                date_of_birth=self.cleaned_data['date_of_birth'],
                address=self.cleaned_data['address'],
                emergency_contact_name_1=self.cleaned_data['emergency_contact_name_1'],
                emergency_contact_phone_1=self.cleaned_data['emergency_contact_phone_1'],
                emergency_contact_priority_1=self.cleaned_data['emergency_contact_priority_1']
            )
        return user


class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']


class HazardReportForm(forms.ModelForm):
    class Meta:
        model = HazardReport
        fields = ['street_name', 'city', 'country', 'description']

from django import forms
from .models import ReportedHazardArea


class ReportHazardForm(forms.ModelForm):
    class Meta:
        model = ReportedHazardArea
        fields = ['name', 'description', 'latitude', 'longitude']

        widgets = {
            'latitude': forms.HiddenInput(),
            'longitude': forms.HiddenInput(),
        }


class HazardCommentForm(forms.ModelForm):
    class Meta:
        model = HazardComment
        fields = ['comment_text']



class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'profile_picture', 'name', 'date_of_birth', 'address', 'favorite_locations',
            'emergency_contact_name_1', 'emergency_contact_phone_1', 'emergency_contact_priority_1',
            'emergency_contact_name_2', 'emergency_contact_phone_2', 'emergency_contact_priority_2',
            'emergency_contact_name_3', 'emergency_contact_phone_3', 'emergency_contact_priority_3'
        ]
        
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }


class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)


from django import forms
from .models import SubscriptionPlan


class PaymentForm(forms.Form):
    plan = forms.ModelChoiceField(queryset=SubscriptionPlan.objects.all(), label="Select Plan")
    payment_method = forms.ChoiceField(
        choices=[
            ('credit_card', 'Credit Card'),
            ('paypal', 'PayPal'),
            ('google_pay', 'Google Pay'),
            ('apple_pay', 'Apple Pay')
        ],
        label="Payment Method"
    )
    promo_code = forms.CharField(required=False, label="Enter Promo Code")
