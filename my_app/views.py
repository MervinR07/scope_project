from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.core.mail import send_mail
from .models import *
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login,logout
from django.contrib.auth.decorators import login_required

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
        if user.profile.email_verified==False:
            messages.error(request,'please verify your email first')
            return redirect('first_time_login')
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

def contact_form(request):
    if request.method=='POST':
        name=request.POST.get('name')
        email=request.POST.get('email')
        subject=request.POST.get('subject')
        message=request.POST.get('message')

        if not name or not email or not subject or not message:
            messages.error(request,'all fields are required')
        ContactMessage.objects.create(
            name=name,
            email=email,
            subject=subject,
            message=message
        )
        try:
            send_mail(
                subject=subject,
                message=message,
                from_email=email,
                recipient_list=['info@scopeindia.org'],
                fail_silently=False
            )
            messages.success(request,'your message has been sent succesfully')
        except:
            messages.error(request,'unable to send email right now please try again later')
        return redirect('contactus')

    return render(request,'contact_form.html')

@login_required
def dashboard(request):
    query=request.GET.get('search')
    if query:
        courses=Course.objects.filter(name_icontains=query)
    else:
        courses=Course.objects.all()
    my_courses=Student_courses.objects.filter(student=request.user)
    context={
        'courses':courses,
        'my_courses':my_courses,
        'query':query
    }
    return render(request,'dashboard.html',context)
@login_required
def signedup_course(request,course_id):
    course=Course.objects.filter(id=course_id).first()
    if not course:
        messages.error(request,'no course found')
        return redirect('dashboard')
    exists=Student_courses.objects.filter(student=request.user,course=course).first()
    if exists:
        messages.error(request,'you have already chosen that course')
        return redirect('dashboard')
    Student_courses.objects.create(
        student=request.user,
        course=course
    )
    messages.success(request,'you have signed up for this course')
    return redirect('dashboard')

@login_required
def edit_profile(request):
    profile = request.user.profile
    user = request.user 

    if request.method == "POST":

        user.first_name = request.POST.get("first_name")
        user.last_name = request.POST.get("last_name")
        user.save()

        profile.phone = request.POST.get("phone")
        profile.city = request.POST.get("city")
        profile.state = request.POST.get("state")
        profile.country = request.POST.get("country")
        profile.hobbies = request.POST.get("hobbies")


        if request.FILES.get("avatar"):
            profile.avatar = request.FILES.get("avatar")

        profile.save()

        messages.success(request, "Profile updated successfully")
        return redirect("edit_profile")

    return render(request, "edit_profile.html", {"profile": profile, "user": user})

@login_required
def change_password(request):

    if request.method=='POST':
        old=request.POST.get('old_password')
        new=request.POST.get('new_password')

        if not request.user.check_password(old):
            messages.error(request,'incorrect old password')
            return redirect('change_password')
        request.user.set_password(new)
        request.user.save()

        logout(request)
        messages.success(request,'passwordword changed successfully please login again')
        return redirect('scopelogin')
    return render(request,'change_password.html')

def logout_user(request):
    logout(request)
    response=redirect('scopelogin')
    response.delete_cookie('remember_me')
    return response

