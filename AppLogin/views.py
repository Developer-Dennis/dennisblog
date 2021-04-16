from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm,PasswordChangeForm
from django.contrib.auth import login,authenticate,logout
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from AppLogin.forms import UserProfileChange,ProfilePic,SignupForm
 




# Create your views here.

def signup(request):
    form = SignupForm()
    registered = False
    if request.method == 'POST':
        form = SignupForm(data=request.POST)
        if form.is_valid():
            form.save()
            registered = True
    dict = {'form':form,'registered':registered}
    return render(request,'AppLogin/signup.html',context=dict)



def loginpage(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username,password=password)
            if user is not None:
                login(request,user)
                return HttpResponseRedirect(reverse('index'))

    return render(request,'AppLogin/login.html',context={'form':form})

@login_required
def logoutuser(request):
    logout(request)
    return HttpResponseRedirect(reverse('AppLogin:signin'))
    
    
@login_required
def Profile(request):
    return render(request,'AppLogin/profile.html',context={})

      
      
@login_required
def userchange(request):
    currentuser = request.user
    form = UserProfileChange(instance=currentuser)
    if request.method == 'POST':
        form = UserProfileChange(request.POST,instance=currentuser)
        if form.is_valid():
            form.save()
            form = UserProfileChange(instance=currentuser)
    return render(request,'AppLogin/changeprofile.html',context={'form':form})
    

@login_required
def passchange(request):
    currentuser = request.user
    changed = False
    form = PasswordChangeForm(currentuser) 
    if request.method == 'POST':
        form = PasswordChangeForm(currentuser,data=request.POST)
        if form.is_valid():
            form.save()
            changed = True
    return render(request,'AppLogin/passchange.html',context={'form':form,'changed':changed})     



@login_required
def AddProfilePic(request):
    form = ProfilePic()
    if request.method == 'POST':
        form = ProfilePic(request.POST,request.FILES)
        if form.is_valid():
            user_obj = form.save(commit=False)
            user_obj.user = request.user
            user_obj.save()
            return HttpResponseRedirect(reverse('AppLogin:profile'))
    return render(request,'AppLogin/profilepic.html' ,context={'form':form})



@login_required
def ChangeProfilePic(request):
    form = ProfilePic(instance=request.user.user_profile)
    if request.method == 'POST':
        form = ProfilePic(request.POST,request.FILES,instance=request.user.user_profile)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('AppLogin:profile'))
    return render(request,'AppLogin/profilepic.html' ,context={'form':form})
