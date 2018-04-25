from django.conf.urls import url
from . import views

urlpatterns = [
    # Admin URLs
    url(r'^admin/$', views.admin), # admin_dash
    # User-Facing URLs
    url(r'^$', views.index), # index
    url(r'^login/$', views.login), # login
    url(r'^register/$', views.register), # register
    url(r'^dashboard/$', views.dashboard), # user_dash
    url(r'^order/$', views.payment_form), # payment_ccform
    url(r'^order-conf/$', views.payment_conf), #payment_conf
    url(r'^treasure/new/$', views.seller_treasure_add), # seller_treasure_add
    # url(r'^treasure/requests$', views.treasure_requests), # renter_requests
    # url(r'^treasure/(?P<treasure_id>\d+$)/requests$', views.treasure_requests), #seller_requests
    url(r'^treasure/(?P<treasure_id>\d+$)', views.treasure_profile), #profile_treasure
    url(r'^treasure/(?P<treasure_id>\d+)/edit/$', views.treasure_edit), #seller_edit_item
    # POST Requests
    url(r'^create_user/$', views.create_user),
    url(r'^login_user/$', views.login_user),
    url(r'^add_treasure/$', views.add_treasure),
    url(r'^update/(?P<treasure_id>\d+)/$', views.update_treasure),
    url(r'^request/(?P<treasure_id>\d+)/$', views.new_request),
    url(r'^checkout/(?P<request_id>\d+)/$', views.checkout),
    # GET Requests
    url(r'^logout/$', views.logout),
    url(r'^delete/(?P<treasure_id>\d+)/$', views.delete),
    # Catch-All
]