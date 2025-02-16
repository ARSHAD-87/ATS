from django.contrib import admin
from django.urls import path , include
from . import views
urlpatterns = [
    path('',views.index,name='index'),
    path('delete/<str:job_id>/', views.delete_job, name='delete_job'),

]


