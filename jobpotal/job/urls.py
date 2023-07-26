from django.urls import path
from job.views import UserLoginView,UserRegistrationView,UserPersonalInfoView



urlpatterns = [
    path('register/', UserRegistrationView.as_view(),name='register'),
    path('login/', UserLoginView.as_view(),name='login'),
    path('profile/', UserPersonalInfoView.as_view(),name='profile'),
    # path('personalinfo/', PersonalInfo.as_view(),name='per')



]