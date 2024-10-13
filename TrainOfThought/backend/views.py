from django.http import JsonResponse
from .models import Bot, Post, Creator
from django.shortcuts import render
from TrainOfThought.scripts.ai import gpt_post_response
from TrainOfThought.scripts.update_vars import update_attributes, get_bot_attributes
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect
from django.core import serializers


def index(request):
    bot = Bot.objects.get(id=0)
    stats = {
        "reputation": int(bot.reputation),
        "hatred": int(bot.hatred),
        "popularity": int(bot.popularity),
        "networth": "{:,.0f}".format(bot.networth / 1_000_000)
    }
    return render(request, "TrainOfThought/index.html", {'stats': stats})

@api_view(["GET", "POST"])
@ensure_csrf_cookie
def gpt_post(request):
    if request.method == 'POST':
        post = request.data.get('user_input')
        person = request.data.get('person')
        response = gpt_post_response(post, person)

        print(response)
        likes, reposts = update_attributes(0, response[0], 0.5)
        print (likes, reposts)
        return Response({'response': response, 'likes': likes, 'reposts': reposts})
    else:
        # Pass through the likes and reposts in a 'data' part from the bot backend
        likes, reposts = get_bot_attributes()
        return render(request, "TrainOfThought/gpt-post.html", {'likes': likes, 'reposts': reposts})

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
        #"image": post_data['image'],
        "likes": post_data['likes'],
        "reposts": post_data['reposts']
    }
    
    if bot.id == 0:
        posts = gpt_post_response(post_data['content'], bot.name)
        created_posts = []
        sentiment = posts[0]

        print("OLD: ", bot.popularity, sentiment)
        # Call Sentiment Updating Script
        likes = update_attributes(0, sentiment, bot.popularity)

        bot = Bot.objects.get(id=post_data['bot'])
        print("NEW: ", bot.popularity)

        stats = []
    

        for post_content in posts[1]:
            data = {
                "bot": 1,
                "content": post_content[0],
                #"image": post_data['image'],
                "likes": post_data['likes'],
                "reposts": post_data['reposts']
            }
            try:
                created_posts.append({
                    "bot": 1,
                    "content": post_content[0],
                    #"image": post_data['image'],
                    "likes": post_data['likes'],
                    "reposts": post_data['reposts'],
                    "name": bot.name
                })
            except Exception as e:
                return JsonResponse({"error": str(e)}, status=400)

        stats.append({
            "reputation": int(bot.reputation),
            "hatred": bot.hatred,
            "popularity": bot.popularity,
            "likeness": bot.likeness,
            "networth": "{:,.0f}".format(bot.networth / 1_000_000)
        })
    
        print (stats)

        return JsonResponse({"message": 'success', "posts": created_posts, "stats": stats}, safe=False)

    return JsonResponse({"message": "Created Successfully"}, safe=False)

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
            my_bot.creator_id = creator

            my_bot.save()

            return JsonResponse({'message': 'Creator selected successfully', 'redirect_url': '/index', 'success': True})

        except Creator.DoesNotExist:
            return JsonResponse({'message': 'Creator not found', 'success': False})


    return JsonResponse({'message': 'Creator selected successfully', 'redirect_url': '/index', 'success': False})


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

@api_view(["POST"])
@csrf_protect
def get_x_posts(request):
    '''
    Get x post random posts
    Parameters:
    num_posts (int): The number of posts to get
    '''
    data = request.data
    x = data['num_posts']
    posts = Post.objects.all().order_by('?')[:x]

    data = []
    for post in posts:
        data.append({
            "id": post.id,
            "bot": post.bot_id,
            "content": post.content,
            "likes": post.likes,
            "reposts": post.reposts
        })
    return JsonResponse(data, safe=False)


@api_view(["GET"])
def get_metrics(request):
    '''
    Get the metrics of the bot

    Returns:
    dict: A dictionary of the bot metrics
    '''


    data = {
        "reputation": 0,
        "hatred": 0,
        "popularity": 0,
        "networth": 0
    }

    try:
        my_bot = Bot.objects.get(id=0)

        data = {
        "reputation": my_bot.reputation,
        "hatred": my_bot.hatred,
        "popularity": my_bot.popularity,
        "networth": my_bot.networth
        }


        return JsonResponse({"metrics" : data , "me" : my_bot.creator_id.first_name + " " + my_bot.creator_id.last_name, "image" : my_bot.creator_id.image.url})
    except Bot.DoesNotExist:
        return JsonResponse({"metrics" : data})