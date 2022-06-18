from email import message
from django.shortcuts import redirect, render

from app.models import OrderPlaced


# Create your views here.



#profile view and profile form

def orderdetail(requrst):
    order_placed=OrderPlaced.objects.all().order_by('-ordered_date')
    
    return render (requrst,'vendor/detail.html',{'order_placed':order_placed})

def delivered(requrst):
    order_placed=OrderPlaced.objects.filter(status='Delivered').order_by('-ordered_date')
    return render (requrst,'vendor/detail.html',{'order_placed':order_placed})

def pending(requrst):
    order_placed=OrderPlaced.objects.filter(status='Pending').order_by('-ordered_date')
    return render (requrst,'vendor/detail.html',{'order_placed':order_placed})
def accepted(requrst):
    order_placed=OrderPlaced.objects.filter(status='Accepted').order_by('-ordered_date')
    return render (requrst,'vendor/detail.html',{'order_placed':order_placed})



#redirct dashboard
def vendordashbord(request):
    return render(request, 'vendor/vendor.html',)



