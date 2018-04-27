# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
import re
import bcrypt
from datetime import datetime, date, timedelta

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    # Login Validator
    def login_validation(self, postData):
        errors = {}
        user = User.objects.filter(email = postData['email'].lower())
        if len(user):
            user = User.objects.filter(email = postData['email'].lower())[0]
        else:
            errors['login'] = "The email or password you entered was incorrect."
            return errors
        password = bcrypt.checkpw(postData['password'].encode(), user.password.encode())
        if password == False:
            errors['password'] = "The email or password you entered was incorrect."
        if errors:
            return errors
    # User Login
    def login_user(self, postData):
        email = (postData['email']).lower()
        user = User.objects.filter(email = email)[0]
        return user
    # Registration Validator
    def reg_validation(self, postData):
        errors = {}
        email = (postData['email']).lower()
        if len(User.objects.filter(email = email)) > 0:
            errors['email'] = "Your email already exists within our system. Please log in."
            return errors
        if len(postData['first_name']) < 1:
            errors['first_name'] = "A first name is required."
        elif len(postData['first_name']) < 2:
            errors['first_name'] = "Your first name is too short."
        if len(postData['last_name']) < 1:
            errors['last_name'] = "A last name is required."
        elif len(postData['last_name']) < 2:
            errors['last_name'] = "Your last name is too short."
        if len(postData['email'].lower()) < 1:
            errors['email'] = "An email is required."
        elif not EMAIL_REGEX.match(postData['email'].lower()):
            errors['email'] = "Your email is not the correct format."
        if len(postData['zip_code']) < 1:
            errors['zip_code'] = "A zip code is required."
        elif len(postData['zip_code']) < 5 or len(postData['zip_code']) > 5:
            errors['zip_code'] = "Your zip code must be exactly 5 characters long."
        if len(postData['password']) < 8:
            errors['password'] = "Your password must be at least 8 characters long."
        elif postData['password'] != postData['pass_conf']:
            errors['password'] = "Your passwords don't match."
        today_year = int(datetime.today().year)
        today_month = int(datetime.today().month)
        today_day = int(datetime.today().day)
        if int(postData['birthday_month']) == 0 or int(postData['birthday_day']) == 0 or int(postData['birthday_year']) == 0:
            errors['birthday'] = "A birthday is required."
        elif int(postData['birthday_year']) == today_year and int(postData['birthday_month']) > today_month:
            errors['birthday'] = "Your birthday must preceed today's date."
        elif int(postData['birthday_month']) == today_month and int(postData['birthday_day']) > today_day:
            errors['birthday'] = "Your birthday must preceed today's date."
        age = today_year - int(postData['birthday_year']) - ((today_month, today_day) < (int(postData['birthday_month']), int(postData['birthday_day'])))
        if age < 18:
            errors['age'] = "Sorry, you're too young. Please ask a parent/guardian to create an account for you."
        return errors
    # Create New User
    def create_user(self, postData):
        first_name = postData['first_name']
        last_name = postData['last_name']
        email = postData['email'].lower()
        zip_code = postData['zip_code']
        birthday = date(int(postData['birthday_year']), int(postData['birthday_month']), int(postData['birthday_day']))
        password = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt())
        if 'user_level' in postData or len(User.objects.all()) < 1:
            if not 'user_level' in postData:
                user_level = 9
            else:
                user_level = postData['user_level']
            new_user = User.objects.create(first_name = first_name, last_name = last_name, email = email, user_level = user_level, zip_code = zip_code, birthday = birthday, password = password)
        else:
            new_user = User.objects.create(first_name = first_name, last_name = last_name, email = email, zip_code = zip_code, birthday = birthday, password = password)
        return new_user

class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.CharField(max_length=255)
    user_level = models.SmallIntegerField(default=1) # 1 = Normal User, 9 = Admin
    zip_code = models.SmallIntegerField()
    birthday = models.DateField()
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class TreasureManager(models.Manager):
    # Add Treasure Validator
    def add_treasure_validation(self, postData):
        errors = {}
        if len(postData['name']) < 1:
            errors['name'] = "An item name is required."
        elif len(postData['name']) < 2:
            errors['name'] = "Your item name is too short."
        if len(postData['desc']) < 1:
            errors['desc'] = "An item description is required."
        elif len(postData['desc']) < 10:
            errors['desc'] = "Your item description must be at least 10 characters long."
        if int(float(postData['daily_rate'])) < 1:
            errors['daily_rate'] = "The daily rate can't be less than $1.00."
        # if postData['category'] == "Category":
        #     errors['category'] = "A category is required."
        if len(postData['pickup_address']) < 1:
            errors['pickup_address'] = "A pickup address is required."
        elif len(postData['pickup_address']) < 5:
            errors['pickup_address'] = "Your pickup address is too short."
        if len(postData['pickup_city']) < 1:
            errors['pickup_city'] = "A pickup city is required."
        elif len(postData['pickup_city']) < 2:
            errors['pickup_city'] = "Your pickup city is too short."
        if postData['pickup_state'] == "":
            errors['pickup_state'] = "A pickup state is required."
        if len(postData['pickup_zip']) < 1:
            errors['pickup_zip'] = "A pickup zip code is required."
        elif len(postData['pickup_zip']) < 5 or len(postData['pickup_zip']) > 5:
            errors['pickup_zip'] = "Your pickup zip code must be exactly 5 characters long."
        return errors
    # Create New Treasure
    def create_treasure(self, postData, fileData, user):
        name = postData['name']
        desc = postData['desc']
        if fileData:
            primary_img = fileData['primary_img']
        else:
           primary_img = 'no-image-available.jpg'
        daily_rate = postData['daily_rate']
        # daily_rate = int(round(float(postData['daily_rate']) * 100))
        # category = postData['category']
        pickup_address = postData['pickup_address']
        pickup_city = postData['pickup_city']
        pickup_state = postData['pickup_state']
        pickup_zip = postData['pickup_zip']
        new_treasure = Treasure.objects.create(name = name, desc = desc, primary_img = primary_img, daily_rate = daily_rate, pickup_address = pickup_address, pickup_city = pickup_city, pickup_state = pickup_state, pickup_zip = pickup_zip, uploader = user)
        return new_treasure
    def update_treasure(self, postData, fileData, treasure_id):
        treasure = Treasure.objects.get(id=treasure_id)
        treasure.name = postData['name']
        treasure.desc = postData['desc']
        if fileData:
            treasure.primary_img = fileData['primary_img']
        treasure.daily_rate = postData['daily_rate']
        # treasure.category = postData['category']
        treasure.pickup_address = postData['pickup_address']
        treasure.pickup_city = postData['pickup_city']
        treasure.pickup_state = postData['pickup_state']
        treasure.pickup_zip = postData['pickup_zip']
        treasure.save()

class Treasure(models.Model):
    name = models.CharField(max_length=255)
    desc = models.TextField(max_length=1000)
    primary_img = models.ImageField()
    daily_rate = models.CharField(max_length=255)
    uploader = models.ForeignKey(User, related_name="treasures")
    pickup_address = models.CharField(max_length=255, default="")
    pickup_city = models.CharField(max_length=255, default="")
    pickup_state = models.CharField(max_length=2, default="")
    pickup_zip = models.SmallIntegerField(default=0)
    # status = models.SmallIntegerField(default=0)
    # STATUS: 0 = available now, 1 = unavailable now
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = TreasureManager()

# class CategoryManager(models.Manager):
#     # Add Category Validator
#     def add_category_validation(self, postData):
#         errors = {}
#         if len(postData['name']) < 1:
#             errors['name'] = "A category name is required."
#         elif len(postData['name']) < 5:
#             errors['name'] = "Your category name is too short."
#         if len(postData['desc']) < 1:
#             errors['desc'] = "A category  description is required."
#         elif len(postData['desc']) < 25:
#             errors['desc'] = "Your category description must be at least 15 characters long."
#         return errors
#     # Create New Category
#     def create_category(self, postData):
#         name = postData['first_name']
#         desc = postData['last_name']
#         new_category = Category.objects.create(name = name, desc = desc)
#         return new_category

# class Category(models.Model):
#     name = models.CharField(max_length=255)
#     desc = models.TextField(max_length=1000)
#     treasure = models.ForeignKey(Treasure, related_name="categories")
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     objects = CategoryManager()

class RequestManager(models.Manager):
    # Add Request Validator
    def request_validation(self, postData):
        errors = {}
        today = datetime.today().date()
        if not postData['pickup_date']:
            errors['pickup_date'] = "You must select a pickup date."
        else:
            pickup_date = datetime.strptime(postData['pickup_date'],'%Y-%m-%d').date()
            if today > pickup_date:
                errors['pickup_date'] = "You entered a pickup date that was in the past."
        if int(postData['days']) < 1:
            errors['days'] = "You cannot borrow an item for less than a day."
        return errors
    # Create New Request
    def create_request(self, postData, treasure_id, user_id):
        days = int(postData['days']) * 1.00
        treasure = Treasure.objects.get(id = treasure_id)
        amount = "%.2f" % round(float(treasure.daily_rate) * days,2)
        requester = User.objects.get(id = user_id)
        pickup_date = postData['pickup_date']
        Request.objects.create(days = days, amount = amount, requester = requester, treasure = treasure, pickup_date = pickup_date)
    def update_request(self, postData, request_id):
        this_request = Request.objects.get(id=request_id)
        treasure = this_request.treasure
        this_request.days = int(postData['days']) * 1.00
        this_request.amount = "%.2f" % round(float(treasure.daily_rate) * this_request.days,2)
        this_request.pickup_date = postData['pickup_date']
        this_request.save()
    def accept_request(self, request_id):
        this_request = Request.objects.get(id=request_id)
        this_request.status = 1
        this_request.save()
    def decline_request(self, request_id):
        this_request = Request.objects.get(id=request_id)
        this_request.status = 2
        this_request.save()
    def cancel_request(self, request_id):
        this_request = Request.objects.get(id=request_id)
        this_request.status = 0
        this_request.save()

class Request(models.Model):
    amount = models.CharField(max_length=255)
    days = models.PositiveIntegerField()
    requester = models.ForeignKey(User, related_name="requests")
    treasure = models.ForeignKey(Treasure, related_name="requests")
    request_date = models.DateField(auto_now=True)
    pickup_date = models.DateField()
    status = models.SmallIntegerField(default = 0)
    # STATUS: 0 = Pending, 1 = Accepted, 2 = Declined, 3 = Paid
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = RequestManager()

class OrderManager(models.Manager):
    # Create New Order
    def create_order(self, postData, this_request):
        amount = int(round(float(this_request.amount) * 100))
        days = this_request.days
        renter = this_request.requester
        treasure = this_request.treasure
        pickup_date = this_request.pickup_date
        return_date = pickup_date+timedelta(days=days)
        new_order = Order.objects.create(amount = amount, days = days, renter = renter, treasure = treasure, pickup_date = pickup_date, return_date = return_date)
        return new_order
    def add_token(self, addData):
        Order.objects.get(id=addData['order_id']).add(stripe_token = addData['stripeToken'])

class Order(models.Model):
    charge_id = models.CharField(max_length=255, blank=True)
    amount = models.PositiveIntegerField()
    days = models.PositiveIntegerField()
    renter = models.ForeignKey(User, related_name="orders")
    treasure = models.ForeignKey(Treasure, related_name="orders")
    pickup_date = models.DateField()
    return_date = models.DateField()
    status = models.SmallIntegerField(default = 0)
    # STATUS: 0 = Paid, 1 = With Renter, 2 = Cancelled by Renter, 3 = Cancelled by Uploader, 4 = Finalized
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = OrderManager()