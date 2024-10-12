from django.http import JsonResponse
from .models import Bot, Post
from django.http import JsonResponse
from .models import Bot, Post
from django.shortcuts import render
from TrainOfThought.scripts.ai import gpt_post_response
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_protect

def index(request):
    return render(request, "TrainOfThought/index.html")

@api_view(["POST"])
@csrf_protect
def gpt_post(request):
    if request.method == 'POST':
        post = request.POST['user_input']
        person = request.POST['person']
        response = gpt_post_response(post, person)
        #response = "This is a placeholder response"
        return render(request, "TrainOfThought/gpt-post.html", {'response': response})
    else:
        return render(request, "TrainOfThought/gpt-post.html")

@api_view(["POST"])
@csrf_protect

def create_post(request):
    '''
    Create a new post

    Parameters:
    bot (int): The bot that created the post
    content (str): The content of the post
    image (str): The image of the post
    likes (int): The number of likes the post has
    reposts (int): The number of reposts the post has
    '''
    post_data = request.data
    
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

#update likes or reposts
@api_view(["PUT"])
@csrf_protect   
def update_post(request, post_id):
    '''
    Update a post

    Parameters:
    likes (int): The number of likes the post has
    reposts (int): The number of reposts the post has
    '''
    post_data = request.data

    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post does not exist"}, status=404)
    
    post.likes = post_data['likes']
    post.reposts = post_data['reposts']

    try:
        post.save()
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)
    
    return JsonResponse({"success": "Post updated successfully"}, safe=False)

#get posts
@api_view(["GET"])
@csrf_protect
def get_posts(request):
    '''
    Get all posts

    Returns:
    list: A list of all posts
    '''
    posts = Post.objects.all()
    data = []
    for post in posts:
        data.append({
            "id": post.id,
            "bot": post.bot.id,
            "content": post.content,
            "likes": post.likes,
            "reposts": post.reposts
        })
    return JsonResponse(data, safe=False)