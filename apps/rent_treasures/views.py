# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect, HttpResponse
from models import User, UserManager, Treasure, TreasureManager, Request, RequestManager, Order, OrderManager
from django.contrib import messages
from Borrowdom import settings
import stripe
stripe.api_key = settings.STRIPE_SECRET_KEY

# Admin URLs
def admin(request):
    return HttpResponse("Admin Portal Coming Soon")

# User-Facing URLs
def index(request):
    if not 'user_id' in request.session:
        context = {
            'recent_treasures': Treasure.objects.all().order_by('id').reverse()[:4],
            'available_treasures': Treasure.objects.all().filter(status = 0).order_by('?')[:10],
        }
    else:
        user = User.objects.get(id=request.session['user_id'])
        context = {
            'recent_treasures': Treasure.objects.all().exclude(uploader = user).order_by('id').reverse()[:4],
            'available_treasures': Treasure.objects.all().exclude(uploader = user).filter(status = 0).order_by('?')[:8],
        }
    return render(request, 'rent_treasures/index.html', context)

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
    context = {
        'user': User.objects.get(id=request.session['user_id']),
        'my_treasures': Treasure.objects.filter(uploader=User.objects.get(id=request.session['user_id'])),
        'my_requests': Request.objects.filter(requester=User.objects.get(id=request.session['user_id'])),
    }
    return render(request, 'rent_treasures/user_dash.html', context)

def seller_treasure_add(request):
    if not 'user_id' in request.session:
        return redirect('/')
    return render(request, 'rent_treasures/seller_treasure_add.html')

def treasure_profile(request, treasure_id):
    print Treasure.objects.get(id=treasure_id).daily_rate
    context = {
        'user': User.objects.get(id=request.session['user_id']),
        'treasure': Treasure.objects.get(id=treasure_id),
        'treasure_cost': Treasure.objects.get(id=treasure_id).daily_rate,
    }
    return render(request, 'rent_treasures/profile_treasure.html', context)

def treasure_edit(request, treasure_id):
    context = {
        'treasure': Treasure.objects.get(id=treasure_id),
    }
    return render(request, 'rent_treasures/seller_treasure_edit.html', context)

# def payment_form(request, request_id):
def payment_form(request):
    context = {
        'stripe_key': settings.STRIPE_PUBLIC_KEY,
        # 'request': Request.objects.get(id=request_id),
    }
    return render(request, 'rent_treasures/payment_ccform.html', context)

def payment_conf(request):
    return render(request, 'rent_treasures/payment_conf.html')

# POST Requests
def create_user(request):
    if not 'user_id' in request.session:
        return redirect('/')
    elif request.method != 'POST':
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
    if not 'user_id' in request.session:
        return redirect('/')
    elif request.method != 'POST':
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

def add_treasure(request):
    if not 'user_id' in request.session:
        return redirect('/')
    elif request.method != 'POST':
        return redirect('/')
    errors = Treasure.objects.add_treasure_validation(request.POST)
    if errors:
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
        return redirect('/treasure/new')
    else:
        user = User.objects.get(id = request.session['user_id'])
        treasure = Treasure.objects.create_treasure(request.POST, user)
        return redirect('/treasure/{}'.format(treasure.id))

def update_treasure(request, treasure_id):
    if not 'user_id' in request.session:
        return redirect('/')
    elif request.method != 'POST':
        return redirect('/')
    elif Treasure.objects.get(id=treasure_id):
        uploader_id = Treasure.objects.get(id=treasure_id).uploader.id
    errors = Treasure.objects.add_treasure_validation(request.POST)
    if errors:
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
        return redirect('/treasure/{}/edit'.format(treasure_id))
    elif request.session['user_id'] == uploader_id:
        Treasure.objects.update_treasure(request.POST, treasure_id)
        return redirect('/treasure/{}'.format(treasure_id))
    else:
        return redirect('/')

def new_request(request, treasure_id):
    user_id = request.session['user_id']
    new_request = Request.objects.create_request(request.POST, treasure_id, user_id)
    return redirect('/order/{}'.format(new_request.id))

def checkout(request):
    Request.objects.add_token(request.POST)
    borrowData = {
        'new_request': Request.objects.get(id=request.POST['request_id']),
    }
    new_order = Order.objects.create_order(request.POST, borrowData)
    return redirect('/order-conf/{}'.format(new_order.id))

def accept_request(request, order_id):
    order = Order.objects.get(id=order_id)
    stripe.Charge.create(
        amount=order['amount'],
        currency="usd",
        source=order['stripeToken'],
        description="Charge for order #"+str(order.id),
    )
    return redirect('/treasure/requests/{}'.format(order['treasure'].id))

# GET Requests
def logout(request):
    request.session.clear()
    return redirect('/')

def delete(request, treasure_id):
    if not 'user_id' in request.session:
        return redirect('/')
    elif Treasure.objects.get(id=treasure_id):
        uploader_id = Treasure.objects.get(id=treasure_id).uploader.id
    if request.session['user_id'] == uploader_id:
        Treasure.objects.get(id=treasure_id).delete()
        return redirect('/dashboard')
    else:
        return redirect('/')