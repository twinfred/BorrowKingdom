from django.conf.urls import url
from . import views

urlpatterns = [
    # Admin URLs
    url(r'^bka/$', views.admin), # admin_dash
    # User-Facing URLs
    url(r'^$', views.index), # index
    url(r'^login/$', views.login), # login
    url(r'^register/$', views.register), # register
    url(r'^dashboard/$', views.dashboard), # user_dash
    url(r'^request/(?P<request_id>\d+)/pay/$', views.payment_form), # payment_ccform
    url(r'^order/(?P<order_id>\d+)/$', views.payment_conf), #payment_conf
    url(r'^treasure/new/$', views.seller_treasure_add), # seller_treasure_add
    url(r'^request/(?P<request_id>\d+)/edit/$', views.edit_request), # renter_request_edit
    url(r'^treasure/(?P<treasure_id>\d+)/requests/$', views.treasure_requests), #seller_treasure_requests
    url(r'^treasure/(?P<treasure_id>\d+$)', views.treasure_profile), #profile_treasure
    url(r'^treasure/(?P<treasure_id>\d+)/edit/$', views.treasure_edit), #seller_edit_item
    # POST Requests
    url(r'^create_user/$', views.create_user),
    url(r'^login_user/$', views.login_user),
    url(r'^add_treasure/$', views.add_treasure),
    url(r'^update/(?P<treasure_id>\d+)/$', views.update_treasure),
    url(r'^request/(?P<treasure_id>\d+)/$', views.new_request),
    url(r'^request/(?P<request_id>\d+)/update/$', views.update_request),
    url(r'^checkout/$', views.checkout),
    # GET Requests
    url(r'^logout/$', views.logout),
    url(r'^treasure/(?P<treasure_id>\d+)/delete/$', views.delete),
    url(r'^request/(?P<request_id>\d+)/delete/$', views.delete_request),
    url(r'^request/(?P<request_id>\d+)/accept/$', views.accept_request),
    url(r'^request/(?P<request_id>\d+)/decline/$', views.decline_request),
    url(r'^request/(?P<request_id>\d+)/cancel/$', views.cancel_request),
    url(r'^order/(?P<order_id>\d+)/pickup/$', views.pickup_order),
    url(r'^order/(?P<order_id>\d+)/finalize/$', views.finalize_order),
    # Catch-All
]