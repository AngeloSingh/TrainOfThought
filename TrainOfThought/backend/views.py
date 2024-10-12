from django.http import JsonResponse
from .models import Bot, Post
from django.shortcuts import render
from TrainOfThought.scripts.ai import gpt_post_response
from django.http import JsonResponse
from .models import Bot, Post

def get_posts(request):
    # TODO: Fetch posts
    return JsonResponse(["test", "test"], safe=False)

def evaluate_post(request):
    # TODO: evaluates post passed in
    return JsonResponse(["test", "test"], safe=False)

def create_post(request):
    # TODO: Gets user post and sends to database
    #get request data

    post_data = request.POST
    
    
    try:
        bot = Bot.objects.get(id=post_data['bot'])
    except Bot.DoesNotExist:
        return JsonResponse({"error": "Bot does not exist"}, status=404)
    

    data = {
        "bot": bot,
        "content": post_data['content'],
        "image": post_data['image'],
        "likes": post_data['likes'],
        "reposts": post_data['reposts']
    }

    try:
        post = Post.objects.create(**data)
        post.save()
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)
    
    return JsonResponse({"success": "Post created successfully"}, safe=False)

def generate_post(request):
    # TODO: ChatGPT post
    return JsonResponse(["test", "test"], safe=False)

def tick_posts(request):
    # Fetch recent posts, then updates posts and users, and saves
    # data = list(YourModel.objects.values())
    return JsonResponse(["test", "test"], safe=False)

def index(request):
    return render(request, "TrainOfThought/index.html")

def gpt_post(request):
    if request.method == 'POST':
        post = request.POST['user_input']
        person = request.POST['person']
        response = gpt_post_response(post, person)
        #response = "This is a placeholder response"
        return render(request, "TrainOfThought/gpt-post.html", {'response': response})
    else:
        return render(request, "TrainOfThought/gpt-post.html")
    
def get_posts(request):
    # TODO: Fetch posts
    return JsonResponse(["test", "test"], safe=False)

def evaluate_post(request):
    # TODO: evaluates post passed in
    return JsonResponse(["test", "test"], safe=False)

def create_post(request):
    # TODO: Gets user post and sends to database
    #get request data

    post_data = request.POST
    
    
    try:
        bot = Bot.objects.get(id=post_data['bot'])
    except Bot.DoesNotExist:
        return JsonResponse({"error": "Bot does not exist"}, status=404)
    

    data = {
        "bot": bot,
        "content": post_data['content'],
        "image": post_data['image'],
        "likes": post_data['likes'],
        "reposts": post_data['reposts']
    }

    try:
        post = Post.objects.create(**data)
        post.save()
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)
    
    return JsonResponse({"success": "Post created successfully"}, safe=False)

def generate_post(request):
    # TODO: ChatGPT post
    return JsonResponse(["test", "test"], safe=False)

def tick_posts(request):
    # Fetch recent posts, then updates posts and users, and saves
    # data = list(YourModel.objects.values())
    return JsonResponse(["test", "test"], safe=False)