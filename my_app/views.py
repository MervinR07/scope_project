from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.core.mail import send_mail
from .models import *
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login

def home(request):
    return render(request,'home.html')

def aboutus(request):
    return render(request,'aboutus.html')
def registration(request):
    if request.method == 'POST':

        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        dob = request.POST.get('dob')
        gender = request.POST.get('gender')
        phone = request.POST.get('mobile')
        email = request.POST.get('email')
        country = request.POST.get('country')
        state = request.POST.get('state')
        city = request.POST.get('city')
        hobbies = request.POST.getlist('hobbies') 
        avatar = request.FILES.get('avatar')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists')
            return redirect('registration')

    
        user = User.objects.create(
            username=email,
            email=email,
            first_name=first_name,
            last_name=last_name,
        )
        user.set_unusable_password()
        user.save()

        profile = Profile.objects.create(
            user=user,
            gender=gender,
            dob=dob,
            phone=phone,
            country=country,
            state=state,
            city=city,
            hobbies=", ".join(hobbies),
            avatar=avatar,
        )

        verify_link = f"http://127.0.0.1:8000/my_app/verify/{profile.email_token}/"

        send_mail(
            subject="Your Email verification link",
            message=f"Click to verify your email: {verify_link}",
            from_email="mervinr2002@gmail.com",
            recipient_list=[email],
        )

        messages.success(request, "Registration successful, please verify email!")
        return redirect('registration')

    return render(request, 'registration.html')


def verify(request,token):
    profile=Profile.objects.filter(email_token=token).first()
    if profile:
        profile.email_verified=True
        profile.save()
        messages.success(request,"email verified successfully")
    else:
        messages.error(request,"invalid verification link")
        
    return redirect('scopelogin')

def contactus(request):
    return render(request,'contactus.html')
def scopelogin(request):
    saved_email=request.COOKIES.get('remember_me','')
    if request.method=='POST':
        email=request.POST.get('email')
        password=request.POST.get('password')
        temp_password=request.POST.get('temp_password')
        remember_me=request.POST.get('remember_me')
        
        user=User.objects.filter(email=email).first()
        if not user:
            messages.error(request,"email not registered")
            return redirect('scopelogin')
        
        profile=user.profile

        if temp_password:
            if str(profile.temp_password)==str(temp_password):
                request.session['reset_user']=user.id
                return redirect('create_new_password')
            else:
                messages.error(request,'invalid temporary password')
                return redirect('scopelogin')
            
        user=authenticate(username=email,password=password)

        if user:
            login(request,user) 
            response=redirect('dashboard')

            if remember_me:
                response.set_cookie('remember_me',email,max_age=7*24*60*60)
            else:
                response.delete_cookie('remember_me')
            
            return response
        else:
            messages.error(request,'invalid cardentials')
            return redirect('scopelogin')
            
    return render(request, "scopelogin.html", {"saved_email": saved_email})
def forgot_password(request):
    return render(request,'forgot_password.html')
def first_time_login(request):
    if request.method=='POST':
        email=request.POST.get('email')
        user=User.objects.filter(email=email).first()
        if not user:
            messages.error(request,'email not registered')
            return redirect('scopelogin')
        
        temp_pass=str(uuid.uuid4())[:8]
        user.profile.temp_password=temp_pass
        user.profile.save()
        send_mail(
            subject="temporary password",
            message=f"your temporary password is{temp_pass}",
            from_email="mervinr2002@gmail.com",
            recipient_list=[email],
            fail_silently=False
        )
        messages.success(request,'temporary password send to your mail')
        return redirect('scopelogin')
   

    return render(request,'first_time_login.html')
    
def create_new_password(request):
    user_id=request.session.get('reset_user')
    if not user_id:
        return redirect('scopelogin')
    user=User.objects.get(id=user_id)
    if request.method=='POST':
        password1=request.POST.get('password1')
        password2=request.POST.get('password2')
        if password1!=password2:
            messages.error(request,'passwords must match')
            return redirect('create_new_password')
        user.set_password(password1)
        user.save()
        user.profile.temp_password=None
        user.profile.save()
        del request.session['reset_user']
        messages.success(request,'password created successfully please login')
        return redirect('scopelogin')
    return render(request,'create_new_password.html')
def dashboard(request):
    return render(request,'dashboard.html')
