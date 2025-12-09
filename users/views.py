from django.contrib.auth import login, logout
from django.shortcuts import render,redirect
from .forms import UserRegisterForm, UserloginForm


def sign_up(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('store:store')
    else:
        form = UserRegisterForm()
    return render(request, 'sign_up.html', {'form': form})


def sign_in(request):
    if request.method == 'POST':
        form = UserloginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('store:store')
    else:
        form = UserloginForm()
    return render(request, 'sign_in.html', {'form': form})


def sign_out(request):
    logout(request)
    return redirect('users:sign_in')