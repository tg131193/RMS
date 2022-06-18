from django.urls import path
from vendor import views
app_name='vendor'
urlpatterns = [
   
   
    path('vendordashbord',views.vendordashbord,name='vendordashbord'),
   
    
   
   
    
   
   path('detail/order',views.orderdetail,name='detail'),
   path('detail/delivered',views.delivered,name='delivered'),
   path('detail/accepted',views.accepted,name='accepted'),
   path('detail/pending',views.pending,name='pending'),





    
]
