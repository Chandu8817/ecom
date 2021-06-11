from django.urls import path
from django.contrib.auth.decorators import login_required

from . import views
from account.views import (UserSignUpView, UserLoginView, UserLogoutView,
                           AccountView,  UpdateProfilePhoto)

urlpatterns = [

    path('login/', UserLoginView.as_view(), name='login'),
    path('profile/', AccountView.as_view(), name='profile'),
    path('signup/', UserSignUpView.as_view(), name='signup'),
    path('logout', UserLogoutView.as_view(), name='logout'),
    path('update/', UpdateProfilePhoto.as_view(), name='update'),
    path('tracking/', views.Tracking.as_view(), name='tracking'),

    # path('signup/', views.signup, name="signup"),
    path('activate/<uidb64>/<token>/',views.activate, name='activate'),
]
