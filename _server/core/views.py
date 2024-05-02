from django.shortcuts import render
from django.conf  import settings
import json
import os
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.forms.models import model_to_dict
from .models import UserProfile, Post
from django.utils import timezone

# Load manifest when server launches
MANIFEST = {}
if not settings.DEBUG:
    f = open(f"{settings.BASE_DIR}/core/static/manifest.json")
    MANIFEST = json.load(f)

# Create your views here.
@login_required
def index(req):
    context = {
        "asset_url": os.environ.get("ASSET_URL", ""),
        "debug": settings.DEBUG,
        "manifest": MANIFEST,
        "js_file": "" if settings.DEBUG else MANIFEST["src/main.ts"]["file"],
        "css_file": "" if settings.DEBUG else MANIFEST["src/main.ts"]["css"][0]
    }
    return render(req, "core/index.html", context)

@login_required
def me(req):
    return JsonResponse({"user": model_to_dict(req.user)})

@login_required
def my_profile(req):
    if req.method == 'GET':
        return JsonResponse({"profile": model_to_dict(req.user.userprofile)})
    elif req.method == 'POST':
        profile = req.user.userprofile
        data = json.loads(req.body)
        
        # Update fields only if they are present in the request
        cat_breed = data.get('cat_breed')
        if cat_breed is not None:
            profile.cat_breed = cat_breed
        
        link_to_pfp = data.get('link_to_pfp')
        if link_to_pfp is not None:
            profile.link_to_pfp = link_to_pfp

        bio = data.get('bio')
        if bio is not None:
            profile.bio = bio
        
        # Save the profile after making changes
        profile.save()
        return JsonResponse({"profile": model_to_dict(profile)})

@login_required
def make_post(request):
    if request.method == 'POST':
        # Parse the JSON body of the request
        data = json.loads(request.body)
        caption = data.get('caption', '')
        link_to_image = data.get('link_to_image', '')
        # Get the user profile associated with the logged-in user
        user_profile = UserProfile.objects.get(user=request.user)
        
        # Create a new Post instance without setting 'likes'
        new_post = Post.objects.create(
            profile=user_profile,
            caption=caption,
            link_to_image=link_to_image
            # 'likes' should not be included here if it's a computed property
        )
        
        # Save the post
        new_post.save()
        
        return JsonResponse({"message": "Post created successfully"}, status=201)
    else:
        return JsonResponse({"error": "Method not allowed"}, status=405)

# views.py

@login_required
def view_post(request, post_id):
    try:
        # Retrieve the post by ID
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        # If the post does not exist, return an error response
        return JsonResponse({"error": "Post not found"}, status=404)

    # If the post exists, serialize it and return the response
    post_data = model_to_dict(post, fields=['profile', 'caption', 'link_to_image', 'likes'])
    return JsonResponse(post_data)

@login_required
def user_posts(request):
    user_profile = UserProfile.objects.get(user=request.user)
    posts = Post.objects.filter(profile=user_profile).order_by('-id')
    posts_data = [
        {
            "id": post.id,
            "caption": post.caption,
            "link_to_image": post.link_to_image,
            "likes": post.likes,
            "username": post.profile.user.username,
            "profile_picture": post.profile.link_to_pfp,
            "created_at": post.created_at.strftime('%Y-%m-%d %H:%M:%S')  # Format the datetime
        } for post in posts
    ]
    return JsonResponse({"posts": posts_data})

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Post
from datetime import datetime


@login_required
def trending_posts(request):
    posts = Post.objects.all()
    now = timezone.now()  # Use timezone-aware datetime
    for post in posts:
        days_since_posted = (now - post.created_at).days
        post.ranking_score = post.likes / (days_since_posted ** 2 if days_since_posted > 0 else 1)
    sorted_posts = sorted(posts, key=lambda p: p.ranking_score, reverse=True)[:100]
    posts_data = [
        {
            "id": post.id,
            "bio": post.profile.bio,
            "caption": post.caption,
            "link_to_image": post.link_to_image,
            "likes": post.likes,
            "username": post.profile.user.username,
            "profile_picture": post.profile.link_to_pfp,
            "created_at": post.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            "ranking_score": post.ranking_score,
            "liked_by_user": request.user in post.liked_by.all()  # Boolean value whether user liked the post
        } for post in sorted_posts
    ]
    return JsonResponse({"posts": posts_data})

@login_required
def toggle_like_post(request, post_id):
    try:
        post = Post.objects.get(id=post_id)
        user = request.user

        # Check if the user has already liked the post
        if user in post.liked_by.all():
            post.liked_by.remove(user)
        else:
            post.liked_by.add(user)

        post.save()
        return JsonResponse({'likes': post.likes})  # Return the current count of likes

    except Post.DoesNotExist:
        return JsonResponse({'error': 'Post not found'}, status=404)

