from django.urls import path
from . import views

urlpatterns = [
    path('',views.signuppage,name='signup'),
    path('login/',views.loginpage,name='login'),
    path('home/',views.homepage,name='home'),
    path('add/',views.add,name='add'),
    path('add/update/<int:id>',views.update,name='update'),
    path('add/delete/<int:id>',views.delete,name='delete'),
    path('logout/',views.logoutpage,name='logout'),
]

