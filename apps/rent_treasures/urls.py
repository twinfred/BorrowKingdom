from django.conf.urls import url
from . import views

urlpatterns = [
    # Admin URLs
    url(r'^admin$', views.admin), # admin_dash
    # User-Facing URLs
    url(r'^$', views.index), # index
    url(r'^login$', views.login), # login
    url(r'^register$', views.register), # register
    url(r'^dashboard$', views.dashboard), # user_dash
    # url(r'^treasure/new$', views.seller_post), # seller_post
    # url(r'^treasure/requests$', views.treasure_requests), # renter_requests
    # url(r'^treasure/(?P<item_id>\d+$)/requests$', views.treasure_requests), #seller_requests
    # url(r'^treasure/(?P<item_id>\d+$)', views.treasure_profile), #profile_treasure
    # url(r'^treasure/edit/(?P<item_id>\d+)$', views.item_edit), #seller_edit_item
    # url(r'^order$', views.order), #renter_checkout
    # POST Requests
    url(r'^create_user$', views.create_user),
    url(r'^login_user$', views.login_user),
    # GET Requests
    url(r'^logout$', views.logout),
    # Catch-All
]