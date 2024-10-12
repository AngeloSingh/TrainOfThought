from django.http import JsonResponse
from django.shortcuts import render


def index(request):
    return render(request, "TrainOfThought/index.html")

def get_posts(request):
    # TODO: Fetch posts
    return JsonResponse(["test", "test"], safe=False)

def evaluate_post(request):
    # TODO: evaluates post passed in
    return JsonResponse(["test", "test"], safe=False)

def create_post(request):
    # TODO: Gets user post and sends to database
    return JsonResponse(["test", "test"], safe=False)

def generate_post(request):
    # TODO: ChatGPT post
    return JsonResponse(["test", "test"], safe=False)

def tick_posts(request):
    # Fetch recent posts, then updates posts and users, and saves
    # data = list(YourModel.objects.values())
    return JsonResponse(["test", "test"], safe=False)