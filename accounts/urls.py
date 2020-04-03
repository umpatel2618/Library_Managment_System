from django.urls import path 
from . import views
from django.conf.urls import url

app_name = 'accounts'

urlpatterns = [
    path('',views.home,name='home'),
    path('profile/',views.profile,name='profile'),
    path('profile/<int:pk>/update',views.ProfileUpdateView.as_view(),name='profile_update'),
    path('login/',views.LoginView.as_view(),name='login'),
    path('register/', views.RegistrationView.as_view(), name='register'),
    url(r'^ajax/validate_username/$', views.Validate_Username, name='validate_username'),
    path('logout/', views.LogoutView.as_view(), name="logout"),
    
]
