import torch
import torch.nn as nn
import torch.nn.functional as F
from torchvision import transforms
from PIL import Image
import requests
from io import BytesIO
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.http import JsonResponse, HttpResponse


class SimpleCNN(nn.Module):
    def __init__(self):
        super(SimpleCNN, self).__init__()
        self.conv_layers = nn.Sequential(
            nn.Conv2d(3, 16, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2),
            nn.Conv2d(16, 32, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2),
            nn.Conv2d(32, 64, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2),
        )
        self.fc_layers = nn.Sequential(
            nn.Linear(64 * 28 * 28, 512),
            nn.ReLU(),
            nn.Linear(512, 1)
        )

    def forward(self, x):
        x = self.conv_layers(x)
        x = torch.flatten(x, 1)
        x = self.fc_layers(x)
        return x

# Load the model and set transformations
transform = transforms.Compose([
    transforms.Resize((224, 224)),  # Assuming your model expects 224x224 images
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

device = torch.device('cpu')
model = SimpleCNN()
model.load_state_dict(torch.load('./registration/model_feline_classifier.pth'))
model.eval()
model.to(device)


def load_image_from_url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises stored HTTPError, if one occurred
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
        is_cat = prediction.item() > 0.5
        if(is_cat == False):
            print("no cat")
        return is_cat

def is_cat_image(url):
    image = load_image_from_url(url)
    return predict_image(image)


def sign_up(req):
    if req.method == "POST":
        cat_image_url = req.POST.get("cat_image_url")
        if not is_cat_image(cat_image_url):
            return render(req, "registration/sign_up.html", {
                'error': 'The provided URL does not contain a cat image. Please provide a valid cat image URL.'
            })
        
        user = User.objects.create_user(
            username=req.POST.get("username"),
            password=req.POST.get("password"),
            first_name=req.POST.get("first_name"),
            last_name=req.POST.get("last_name"),
        )
        login(req, user)
        return redirect("/")
    else:
        return render(req, "registration/sign_up.html")

def sign_in(req):
    if req.method == "POST":
        user = authenticate(req, username=req.POST.get("username"), password=req.POST.get("password"))
        if user is not None:
            login(req, user)
            return redirect("/")

        return render(req, "registration/sign_in.html",{'error': 'Invalid username or password'})
    else:
        return render(req, "registration/sign_in.html")

def logout_view(request):
    logout(request)
    return JsonResponse({"success": True })
