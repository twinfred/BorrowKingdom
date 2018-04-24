# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect, HttpResponse
from models import User, UserManager, Treasure, TreasureManager, Request, RequestManager
from django.contrib import messages

# Admin URLs
def admin(request):
    return HttpResponse("Admin Portal Coming Soon")

# User-Facing URLs
def index(request):
    return render(request, 'rent_treasures/index.html')

def register(request):
    if 'user_id' in request.session:
        return redirect('/dashboard')
    return render(request, 'rent_treasures/register.html')

def login(request):
    if 'user_id' in request.session:
        return redirect('/dashboard')
    return render(request, 'rent_treasures/login.html')

def dashboard(request):
    if not 'user_id' in request.session:
        return redirect('/')
    return HttpResponse("Dashboard")
    return render(request, 'rent_treasures/user_dash.html')

# POST Requests
def create_user(request):
    if request.method != 'POST':
        return redirect('/')
    errors = User.objects.reg_validation(request.POST)
    if errors:
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
        return redirect('/register')
    else:
        new_user = User.objects.create_user(request.POST)
        request.session['user_id'] = new_user.id
        return redirect('/dashboard')

def login_user(request):
    if request.method != 'POST':
        return redirect('/')
    errors = User.objects.login_validation(request.POST)
    if errors:
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
        return redirect('/login')
    else:
        user = User.objects.login_user(request.POST)
        request.session['user_id'] = user.id
        return redirect('/dashboard')

# GET Requests
def logout(request):
    request.session.clear()
    return redirect('/')