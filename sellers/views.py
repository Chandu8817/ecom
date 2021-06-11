from django.shortcuts import render
from .models import *
from django.views import View


class DashBoard(View):
    def get(self,request):
        data={}
        user=request.user
        seller=Seller.objects.filter(user=request.user).last()
        data['seller']=seller

        return render(request,'sellers/dashboard.html',data)