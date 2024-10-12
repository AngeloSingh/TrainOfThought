from django.http import JsonResponse
from .models import Bot, Creator, Post
from django.http import JsonResponse
from .models import Bot, Post
from django.shortcuts import render
from TrainOfThought.scripts.ai import gpt_post_response
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import redirect

def index(request):
    return render(request, "TrainOfThought/index.html")

@api_view(["POST"])
@csrf_protect
def gpt_post(request):
    if request.method == 'POST':
        post = request.POST['user_input']
        person = request.POST['person']
        response = gpt_post_response(post, person)
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



def homepage(request):
    creators = Creator.objects.all()
    return render(request, 'TrainOfThought/homepage.html', {'creators': creators})



@api_view(["POST"])
@csrf_protect
def select_creator(request):
    if request.method == 'POST':
        id = request.data['creatorId']

        try:
            bot = Bot.objects.get(id=id)

            posts_to_delete = Post.objects.filter(bot=bot)
            posts_to_delete.delete()


            creator = Creator.objects.get(id=id)


            my_bot = Bot.objects.get(id=0)
            my_bot.reputation = creator.default_reputation
            my_bot.hatred = creator.default_hatred
            my_bot.popularity = creator.default_popularity
            my_bot.networth = creator.networth

            my_bot.save()

            return JsonResponse({'message': 'Creator selected successfully', 'redirect_url': '/', 'success': True})

        except Creator.DoesNotExist:
            return JsonResponse({'message': 'Creator not found', 'success': False})


    return JsonResponse({'message': 'Creator selected successfully', 'redirect_url': '/', 'success': False})