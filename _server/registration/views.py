import torch
import torch.nn as nn
import torch.nn.functional as F
from torchvision import transforms, models
from PIL import Image
import requests
from io import BytesIO
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.http import JsonResponse, HttpResponse
from django.db import IntegrityError

# Setup for the pre-trained ResNet model
device = torch.device('cpu')
model = models.resnet18(pretrained=True)
num_ftrs = model.fc.in_features
model.fc = nn.Linear(num_ftrs, 1)  # Modify the fully connected layer for binary classification
model.load_state_dict(torch.load('./registration/model_feline_classifier.pth', map_location=device))
model.eval()
model.to(device)

# Image transformation
transform = transforms.Compose([
    transforms.Resize((224, 224)),  # Resize images to match the model's expected input size
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

def load_image_from_url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        image = Image.open(BytesIO(response.content)).convert('RGB')
        image = transform(image).unsqueeze(0)
        return image
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return None

def predict_image(image):
    if image is None:
        return False
    with torch.no_grad():
        output = model(image.to(device))
        prediction = torch.sigmoid(output)
        return prediction.item() > 0.5

def is_cat_image(url):
    image = load_image_from_url(url)
    return predict_image(image)


def sign_up(req):
    if req.method == "POST":
        username = req.POST.get("username")
        password = req.POST.get("password")
        first_name = req.POST.get("first_name")
        last_name = req.POST.get("last_name")
        cat_image_url = req.POST.get("cat_image_url")

        if User.objects.filter(username=username).exists():
            return render(req, "registration/sign_up.html", {
                'error': 'This username is already taken. Please choose another.'
            })

        if not is_cat_image(cat_image_url):
            return render(req, "registration/sign_up.html", {
                'error': 'The provided URL does not contain a cat image. Please provide a valid cat image URL.'
            })

        try:
            user = User.objects.create_user(
                username=username,
                password=password,
                first_name=first_name,
                last_name=last_name
            )
            login(req, user)
            return redirect("/")
        except IntegrityError:
            return render(req, "registration/sign_up.html", {
                'error': 'An error occurred while creating the account. Please try again.'
            })

    else:
        return render(req, "registration/sign_up.html")

def sign_in(req):
    if req.method == "POST":
        user = authenticate(req, username=req.POST.get("username"), password=req.POST.get("password"))
        if user is not None:
            login(req, user)
            return redirect("/")
        return render(req, "registration/sign_in.html", {'error': 'Invalid username or password'})
    else:
        return render(req, "registration/sign_in.html")

def logout_view(req):
    logout(req)
    return JsonResponse({"success": True})
