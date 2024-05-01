from django.urls import path
from . import views

urlpatterns = [
    path('', view=views.index, name="index"),
    path('me/',view=views.me, name="current user"),
    path('my_profile/',view=views.my_profile, name="current user profile")
]