from django.shortcuts import render
from django.conf  import settings
import json
import os
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.forms.models import model_to_dict

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
