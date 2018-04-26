# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect, HttpResponse
from models import User, UserManager, Treasure, TreasureManager, Request, RequestManager, Order, OrderManager
from django.contrib import messages
from Borrowdom import settings
import stripe
from django.db.models import Q
stripe.api_key = settings.STRIPE_SECRET_KEY

# Admin URLs
def admin(request):
    if not 'user_id' in request.session:
        return redirect('/')
    user = User.objects.get(id=request.session['user_id'])
    if user.user_level != 9:
        return redirect('/dashboard')
    else:
        return HttpResponse("Admin Portal Coming Soon")

# User-Facing URLs
def index(request):
    if not 'user_id' in request.session:
        context = {
            'recent_treasures': Treasure.objects.all().order_by('id').reverse()[:4],
            'available_treasures': Treasure.objects.all().order_by('?')[:10],
        }
    else:
        user = User.objects.get(id=request.session['user_id'])
        context = {
            'recent_treasures': Treasure.objects.all().exclude(uploader = user).order_by('id').reverse()[:4],
            'available_treasures': Treasure.objects.all().exclude(uploader = user).order_by('?')[:8],
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
    user = User.objects.get(id=request.session['user_id'])
    print Order.objects.filter(Q(status=0)&Q(treasure__uploader=user)).all()
    context = {
        'user': user,
        'my_treasures': Treasure.objects.filter(uploader=user),
        'upcoming_pickups': Order.objects.filter(Q(status=0)&Q(treasure__uploader=user)).all().order_by('pickup_date'),
        'borrowed_treasures': Order.objects.filter(Q(status=1)&Q(treasure__uploader=user)).all().order_by('return_date'),
        'my_requests': Request.objects.filter(requester=user).exclude(status=3),
        'my_upcoming_orders': user.orders.filter(status=0),
        'treasures_borrowing': user.orders.filter(status=1),
    }
    return render(request, 'rent_treasures/user_dash.html', context)

def seller_treasure_add(request):
    if not 'user_id' in request.session:
        return redirect('/')
    return render(request, 'rent_treasures/seller_treasure_add.html')

def treasure_profile(request, treasure_id):
    context = {
        'treasure': Treasure.objects.get(id=treasure_id),
    }
    if 'user_id' in request.session:
        context['user'] = User.objects.get(id=request.session['user_id'])
        if len(Treasure.objects.get(id=treasure_id).requests.filter(requester=User.objects.get(id=request.session['user_id']))):
            context['my_request'] = Treasure.objects.get(id=treasure_id).requests.get(requester=User.objects.get(id=request.session['user_id']))
    context['requesters'] = Treasure.objects.get(id=treasure_id).requests.all()
    return render(request, 'rent_treasures/profile_treasure.html', context)

def treasure_edit(request, treasure_id):
    if not 'user_id' in request.session:
        return redirect('/')
    if not len(Treasure.objects.filter(id=treasure_id)):
        return redirect('/')
    user = User.objects.get(id=request.session['user_id'])
    if Treasure.objects.get(id=treasure_id).uploader != user:
        return redirect('/')
    else:
        context = {
            'treasure': Treasure.objects.get(id=treasure_id),
        }
        return render(request, 'rent_treasures/seller_treasure_edit.html', context)

def edit_request(request, request_id):
    if not 'user_id' in request.session:
        return redirect('/')
    if not len(Request.objects.filter(id=request_id)):
        return redirect('/')
    user = User.objects.get(id=request.session['user_id'])
    if Request.objects.get(id=request_id).requester != user:
        return redirect('/')
    else:
        context = {
            "request": Request.objects.get(id=request_id),
            "request_amount": ("%.2f" % round(float(Request.objects.get(id=request_id).amount), 2))
        }
        return render(request, 'rent_treasures/renter_request_edit.html', context)

def treasure_requests(request, treasure_id):
    if not 'user_id' in request.session:
        return redirect('/')
    user = User.objects.get(id=request.session['user_id'])
    if Treasure.objects.get(id=treasure_id).uploader != user:
        return redirect('/')
    if not len(Treasure.objects.filter(id=treasure_id)):
        return redirect('/')
    else:
        context = {
            'treasure': Treasure.objects.get(id=treasure_id),
            'pending_requests': Treasure.objects.get(id=treasure_id).requests.filter(status=0).order_by('pickup_date'),
            'accepted_requests': Treasure.objects.get(id=treasure_id).requests.filter(status=1).order_by('pickup_date'),
            'declined_requests': Treasure.objects.get(id=treasure_id).requests.filter(status=2).order_by('pickup_date'),
        }
        return render(request, 'rent_treasures/seller_treasure_requests.html', context)

def payment_form(request, request_id):
    if not 'user_id' in request.session:
        return redirect('/')
    user = User.objects.get(id=request.session['user_id'])
    if Request.objects.get(id=request_id).requester != user:
        return redirect('/')
    context = {
        'stripe_key': settings.STRIPE_PUBLIC_KEY,
        'request': Request.objects.get(id=request_id),
        'stripe_amt': int(float(Request.objects.get(id=request_id).amount)) * 100
    }
    return render(request, 'rent_treasures/payment_ccform.html', context)

def payment_conf(request, order_id):
    if not 'user_id' in request.session:
        return redirect('/')
    user = User.objects.get(id=request.session['user_id'])
    if Order.objects.get(id=order_id).renter != user:
        return redirect('/')
    else:
        context = {
            'user': User.objects.get(id=request.session['user_id']),
            'order': Order.objects.get(id=order_id),
        }
        return render(request, 'rent_treasures/payment_conf.html', context)

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

def add_treasure(request):
    if not 'user_id' in request.session:
        return redirect('/')
    if request.method != 'POST':
        return redirect('/')
    errors = Treasure.objects.add_treasure_validation(request.POST)
    if errors:
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
        return redirect('/treasure/new')
    else:
        user = User.objects.get(id = request.session['user_id'])
        Treasure.objects.create_treasure(request.POST, request.FILES, user)
        return redirect('/dashboard')

def update_treasure(request, treasure_id):
    if not 'user_id' in request.session:
        return redirect('/')
    if request.method != 'POST':
        return redirect('/')
    if not len(Treasure.objects.filter(id=treasure_id)):
        return redirect('/')
    uploader_id = Treasure.objects.get(id=treasure_id).uploader.id
    errors = Treasure.objects.add_treasure_validation(request.POST)
    if errors:
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
        return redirect('/treasure/{}/edit'.format(treasure_id))
    elif request.session['user_id'] == uploader_id:
        Treasure.objects.update_treasure(request.POST, request.FILES, treasure_id)
        return redirect('/treasure/{}'.format(treasure_id))
    else:
        return redirect('/')

def new_request(request, treasure_id):
    if not 'user_id' in request.session:
        return redirect('/')
    if request.method != 'POST':
        return redirect('/')
    errors = Request.objects.request_validation(request.POST)
    if errors:
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
        return redirect('/treasure/{}'.format(treasure_id))
    user_id = request.session['user_id']
    Request.objects.create_request(request.POST, treasure_id, user_id)
    return redirect('/treasure/{}'.format(treasure_id))

def update_request(request, request_id):
    if not 'user_id' in request.session:
        return redirect('/')
    if request.method != 'POST':
        return redirect('/')
    if not len(Request.objects.filter(id=request_id)):
        return redirect('/')
    user = User.objects.get(id=request.session['user_id'])
    this_request = Request.objects.get(id=request_id)
    if this_request.requester != user:
        return redirect('/')
    print request.POST
    errors = Request.objects.request_validation(request.POST)
    if errors:
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
        return redirect('/request/{}/edit'.format(request_id))
    Request.objects.update_request(request.POST, request_id)
    messages.success(request, 'Your edit was successfully submitted.')
    return redirect('/treasure/{}'.format(this_request.treasure.id))

def checkout(request):
    if not 'user_id' in request.session:
        return redirect('/')
    if request.method != 'POST':
        return redirect('/')
    this_request = Request.objects.get(id=request.POST['request_id'])
    new_order = Order.objects.create_order(request.POST, this_request)
    try:
        charge = stripe.Charge.create(
            amount=new_order.amount,
            currency="usd",
            source=request.POST['stripeToken'],
            description="Charge for order #"+str(new_order.id),
        )
        new_order.charge_id = charge.id
    except stripe.error.CardError as ce:
        messages.error(request, ce)
        return redirect('/request/this_request.id/pay')
    else:
        new_order.save()
        this_request.delete()
    return redirect('/order/{}'.format(new_order.id))

# GET Requests
def logout(request):
    request.session.clear()
    return redirect('/')

def delete(request, treasure_id):
    if not 'user_id' in request.session:
        return redirect('/')
    if Treasure.objects.get(id=treasure_id):
        uploader_id = Treasure.objects.get(id=treasure_id).uploader.id
    if request.session['user_id'] == uploader_id:
        Treasure.objects.get(id=treasure_id).delete()
        return redirect('/dashboard')
    else:
        return redirect('/')

def delete_request(request, request_id):
    if not 'user_id' in request.session:
        return redirect('/')
    if Request.objects.get(id=request_id):
        uploader_id = Request.objects.get(id=request_id).requester.id
    if request.session['user_id'] == uploader_id:
        Request.objects.get(id=request_id).delete()
        return redirect('/dashboard')
    else:
        return redirect('/')

def accept_request(request, request_id):
    if not 'user_id' in request.session:
        return redirect('/')
    if not len(Request.objects.filter(id=request_id)):
        return redirect('/')
    treasure = Request.objects.get(id=request_id).treasure
    if treasure.uploader != User.objects.get(id=request.session['user_id']):
        return redirect('/')
    else:
        Request.objects.accept_request(request_id)
        return redirect('/treasure/{}/requests'.format(treasure.id))

def decline_request(request, request_id):
    if not 'user_id' in request.session:
        return redirect('/')
    if not len(Request.objects.filter(id=request_id)):
        return redirect('/')
    treasure = Request.objects.get(id=request_id).treasure
    if treasure.uploader != User.objects.get(id=request.session['user_id']):
        return redirect('/')
    else:
        Request.objects.decline_request(request_id)
        return redirect('/treasure/{}/requests'.format(treasure.id))

def cancel_request(request, request_id):
    if not 'user_id' in request.session:
        return redirect('/')
    if not len(Request.objects.filter(id=request_id)):
        return redirect('/')
    treasure = Request.objects.get(id=request_id).treasure
    if treasure.uploader != User.objects.get(id=request.session['user_id']):
        return redirect('/')
    else:
        Request.objects.cancel_request(request_id)
        return redirect('/treasure/{}/requests'.format(treasure.id))

def pickup_order(request, order_id):
    if not 'user_id' in request.session:
        return redirect('/')
    if not len(Order.objects.filter(id=order_id)):
        return redirect('/')
    order = Order.objects.get(id=order_id)
    treasure = Order.objects.get(id=order_id).treasure
    if treasure.uploader != User.objects.get(id=request.session['user_id']):
        return redirect('/')
    else:
        order.status = 1
        order.save()
        return redirect('/dashboard')

def finalize_order(request, order_id):
    if not 'user_id' in request.session:
        return redirect('/')
    if not len(Order.objects.filter(id=order_id)):
        return redirect('/')
    order = Order.objects.get(id=order_id)
    treasure = Order.objects.get(id=order_id).treasure
    if treasure.uploader != User.objects.get(id=request.session['user_id']):
        return redirect('/')
    else:
        order.status = 4
        order.save()
        return redirect('/dashboard')