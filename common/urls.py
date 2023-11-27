from django.urls import path
from .import views

 

app_name='common'

urlpatterns =[
    path('index',views.index,name='index'),
    path('employee/worktime',views.worktime,name='worktime'),
    
    ]