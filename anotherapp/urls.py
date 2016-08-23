from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'), # VIEW HOME PAGE
    url(r'^view/$', views.cat, name='view'),  # VIEW FULL MENU
    url(r'^cart/$', views.add_to_cart, name='cart'),  # ADD AN ITEM TO CART, THIS IS AN AJAX CALL
    url(r'^login/$', views.login_user, name='login'),  # LOGS THE USER IN
    url(r'^logout/$', views.logout_user, name='logout'), # LOGS THE USER OUT
    url(r'^create/$', views.create_user, name='create'),  # CREATE A NEW USER
    url(r'^checkout/$', views.checkout, name='checkout'),  # SHOW THE CHECKOUT PAGE
    url(r'^processing/$', views.final_checkout, name='final_checkout'),  # THE FINAL CHECKOUT. THIS IS WHERE THE USER PAYS
    url(r'^successful/$', views.successful_checkout, name='successful_checkout'),  # SHOW THE CHECKOUT PAGE
    url(r'^dashboard/$', views.dashboard, name='dashboard'),  # SHOW THE CHECKOUT PAGE
    url(r'^order/(?P<confirmation>\w+)$', views.order, name='dashboard'),  # SHOW THE CHECKOUT PAGE
    url(r'^category/', views.cat, name='cat'),  # TESTING THE CATEGORY. POSSIBLY NOT FOR PRODUCTION
    # The below code is used for the owner to update the database. Basically by using a series of ajax calls
    url(r'^order/owner/engine/$', views.owner_engine, name="owner_engine"),
    url(r'^order/owner/', views.store_owner_dashboard, name="owner_dashboard"),  # THIS SHOWS THE ORDER INFO FOR STORE OWNER
    url(r'^order/information/$', views.order_information, name='order_information'),
    url(r'^order/details/(?P<session_number>\w+)$', views.grab_cart_details, name='cart_details'),
]

