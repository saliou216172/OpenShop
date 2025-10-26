from django.shortcuts import render, redirect 
from django.contrib.auth import login,logout,authenticate 
from django.contrib.auth.decorators import login_required
from . forms import RegisterForm, LoginForm 


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
    else:
        form = RegisterForm()
    return render(request, "authentication/register.html", {"form": form})



def login_view(request):
    if request.method == "POST":
          form = LoginForm(request, data=request.POST)
          if form.is_valid():
               user = form.get_user()
               login(request, user)
               return redirect("home")
    else:
         form = LoginForm()

    return render(request, "authentication/login.html", {"form": form})


def logout_view(request):
     logout(request)
     return redirect("home")

