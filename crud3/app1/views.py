
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,logout,login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.auth import forms  
from django.shortcuts import redirect, render  
from django.contrib import messages  
from django.contrib.auth.forms import UserCreationForm  
from .forms import CustomUserCreationForm,CrudUserForm,UserUpdateForm
# Create your views here.  

def signuppage(request):
    if 'username' in request.session:
        return redirect('home')  
    if request.method == 'POST':  
        form = CustomUserCreationForm(request.POST)  
        if form.is_valid():
            print('valid')  
            form.save()
            return redirect('login')  
    else:  
        form = CustomUserCreationForm()  
    context = {  
        'form':form  
    }  
    return render(request, 'signup.html', context)


def loginpage(request):
    if 'username' in request.session:
        return redirect('home')
    if request.method == 'POST':
        name = request.POST.get('username')
        passwd = request.POST.get('password1') 

        user = authenticate(request,username=name,password=passwd)

        if user is not None:
            login(request,user)
            if request.user.is_superuser:
                request.session['username']=name
                return redirect('add')
            else:
                request.session['username']=name
                return redirect('home')
        else:
            messages.error(request,"Invalid username or password")
            return HttpResponse('incorrect password')
        
    return render(request, 'login.html')

@login_required(login_url='login')
def homepage(request):
    return render(request,'home.html')

def logoutpage(request):
    logout(request)
    request.session.flush()
    return redirect('login')

@user_passes_test(lambda u: u.is_superuser, login_url='login')
@login_required(login_url='login')
def add(request):
    if request.method=='POST':
        fm=CrudUserForm(request.POST)
        if fm.is_valid():
            fm.save()
        fm=CrudUserForm()
    else:
        fm=CrudUserForm()
    stu=User.objects.all()
    return render(request,'add.html',{'fm':fm,'stu':stu})

@user_passes_test(lambda u: u.is_superuser)
def update(request, id):
        if request.user.is_authenticated:
            if request.method == 'POST':
                stu = User.objects.get(id=id)
                fm = UserUpdateForm(request.POST, instance=stu)
                if fm.is_valid():
                    fm.save()
                    return redirect('add')
            else:
                stu = User.objects.get(id=id)
                fm = UserUpdateForm(instance=stu)
        return render(request, 'update.html', {'fm':fm, 'stu':stu})

def delete(request,id):
    if request.user.is_authenticated:
        fm = User.objects.get(id=id)
        fm.delete()
        return HttpResponseRedirect('/add')



