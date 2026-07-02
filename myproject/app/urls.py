from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('add/', views.add_item),
    path('delete/<int:id>/', views.delete_item),
    path('browse/', views.browse_items, name='browse_items'),
    path('my-reports/', views.my_reports, name='my_reports'),
    path('how-it-works/', views.how_it_works, name='how_it_works'),
    path('contact/', views.contact, name='contact'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('profile/', views.profile, name='profile'),
]
