from django.http import Http404
from django.shortcuts import render
# Import the scripts/ai.py
from .scripts.ai import gpt_post_response


def index(request):
    return render(request, "TrainOfThought/index.html")

def gpt_post(request):
    if request.method == 'POST':
        post = request.POST['user_input']
        person = request.POST['person']
        response = gpt_post_response(post, person)
        return render(request, "TrainOfThought/gpt-post.html", {'response': response})
    else:
        return render(request, "TrainOfThought/gpt-post.html")