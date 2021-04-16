from django.urls import path
from . import views



app_name = 'AppLogin'
urlpatterns = [
    path('signup/',views.signup,name='signup'),
    path('signin/',views.loginpage,name='signin'),
    path('logout/',views.logoutuser,name='logout'),
    path('profile/',views.Profile,name='profile'),
    path('changeprofile/',views.userchange,name='userchange'),
    path('password/',views.passchange,name='passchange'),
    path('change-profile-image/',views.AddProfilePic,name='AddProfilePic'),
    path('change-picture/',views.ChangeProfilePic,name='ChangeProfilePic'),
]
