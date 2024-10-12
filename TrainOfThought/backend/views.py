from django.http import JsonResponse
from .models import Bot, Post
from django.shortcuts import render
from TrainOfThought.scripts.ai import gpt_post_response
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect

def index(request):
    return render(request, "TrainOfThought/index.html")

@api_view(["GET", "POST"])
@ensure_csrf_cookie
def gpt_post(request):
    if request.method == 'POST':
        post = request.data.get('user_input')
        person = request.data.get('person')
        response = gpt_post_response(post, person)
        return Response({'response': response})
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