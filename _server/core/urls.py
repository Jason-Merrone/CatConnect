from django.urls import path
from . import views

urlpatterns = [
    path('', view=views.index, name="index"),
    path('me/',view=views.me, name="current user"),
    path('my_profile/',view=views.my_profile, name="current user profile"),
    path('make_post/',view=views.make_post, name="user post"),
    path('view_post/',view=views.make_post, name="view post"),
    path('user_posts/', view=views.user_posts, name='user_posts'),
    path('trending/', view=views.trending_posts, name='trending_posts'),
    path('toggle_like_post/<int:post_id>/', view=views.toggle_like_post, name='toggle_like_post'),
]