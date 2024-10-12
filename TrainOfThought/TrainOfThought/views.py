from django.http import Http404
from django.shortcuts import render
# Import the scripts/ai.py
from .scripts.ai import gpt_post_response
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

def index(request):
    return render(request, "TrainOfThought/index.html")

@csrf_exempt
def gpt_post(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        post = data.get('user_input')
        person = data.get('person')
        response = gpt_post_response(post, person)
        return JsonResponse({'response': response})
    else:
        return render(request, "TrainOfThought/gpt-post.html")