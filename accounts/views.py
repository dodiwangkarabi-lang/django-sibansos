from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import RegisterForm, MasyarakatForm

from .services import registrasi_service

def register(request):
    if request.method == "POST":
        user_form = RegisterForm(request.POST)
        masyarakat_form = MasyarakatForm(request.POST)
        if user_form.is_valid() and masyarakat_form.is_valid():
            data = {
                "username": user_form.cleaned_data["username"],
                "password": user_form.cleaned_data["password"],
                "nik": masyarakat_form.cleaned_data["nik"],
                "nama": masyarakat_form.cleaned_data["nama"],
            }
            user = registrasi_service(data)
            login(request, user)
            return redirect("dashboard_masyarakat")
    else:
        user_form = RegisterForm()
        masyarakat_form = MasyarakatForm()
        
    context = {
        "user_form": user_form,
        "masyarakat_form": masyarakat_form
    }
    return render(request, 'pages/register.html', context)

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            
            # cek role
            if user.is_superuser:
                return redirect("admin:index")
            
            elif user.groups.filter(name="masyarakat").exists():
                return redirect("dashboard_masyarakat")
            elif user.groups.filter(name="admin").exists():
                return redirect("dashboard_admin")
            else:
                return redirect("index")
            
        else:
            return render(request, 'pages/login.html', {"error": "Username atau password salah"})
        
    return render(request, 'pages/login.html')
