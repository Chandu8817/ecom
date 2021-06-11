from  django.urls import path
from . import views

urlpatterns = [
    path('dashborad/',views.DashBoard.as_view(),name='dashboard'),
]
