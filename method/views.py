from django.shortcuts import render
from django.shortcuts import render, redirect
from django.views import View
from .forms import UserRegistrationForm, UserLoginForm
from django.contrib import messages
import random
from twilio.rest import Client
from Otp import settings
from django.contrib.auth import get_user_model
# Create your views here.
class OTPVerificationView(View):
    def post(self, request):
        submitted_otp = request.POST.get('otp')
        saved_otp = request.session.get('otp')
        password = request.session.get('password')
        
        if submitted_otp == saved_otp:
            messages.success(request, "OTP verification successful")
            phone_number = request.session.get('phone_number')
            User = get_user_model()
            user = User.objects.create(phone_number=phone_number)
            user.set_password(password)
            user.save()
            return redirect('user_login')
        else:
            messages.error(request, "Invalid OTP. Please try again.")
            return redirect('otp_verification')

class UserRegistrationView(View):
    def get(self, request):
        form = UserRegistrationForm()
        return render(request, 'registeration.html', {'form': form, 'otp_required': False})

    def post(self, request):
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            phone_number = str(form.cleaned_data['phone_number'])
            verification_method = form.cleaned_data['verification_method']

            if 'otp' in request.POST:
                return OTPVerificationView.as_view()(request)
            else:
                password = form.cleaned_data['password']
                otp = generate_otp()

                if verification_method == 'sms':
                    send_sms_otp(phone_number, otp)

                request.session['otp'] = otp
                request.session['phone_number'] = phone_number
                request.session['password'] = password
                form.fields['password'].widget.attrs['value'] = password

                return render(request, 'login.html', {'form': form, 'otp_required': True, 'password': password})

        return render(request, 'registeration.html', {'form': form, 'otp_required': False})

class UserLoginView(View):
    def get(self, request):
        form = UserLoginForm()
        return render(request, 'login.html', {'form': form})
    
    
    def post(self, request):
        form = UserLoginForm(request.POST)
        if form.is_valid():
            messages.success(request,'Login SuccessFul')
            mobile_number = form.cleaned_data['phone_number']
            password = form.cleaned_data['password']
            otp = form.cleaned_data['otp']
            
        
        return render(request, 'login.html',{'form':form})

def generate_otp():
    return str(random.randint(100000, 999999))

def send_sms_otp(phone_number, otp):
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    message = client.messages.create(
        body=f'Your OTP is: {otp}',
        from_=settings.TWILIO_PHONE_NUMBER,
        to=phone_number
    )