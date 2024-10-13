import random
from backend.models import Bot  # Adjust the import according to your project structure

def update_attributes(bot_id, gpt_score, relevance):
    bot = Bot.objects.get(id=bot_id)
    reputation = bot.reputation
    likes = bot.likeness
    popularity = bot.popularity  # Assuming you want to update popularity as reposts

    print(reputation, likes, popularity)
    gpt_score = gpt_score / 100  # Normalize gpt_score to be between -0.1 and 0.1
    relevance = relevance / 100  # Normalize relevance to be between 0 and 0.1
    likes += popularity * gpt_score * random.uniform(0.8, 1.2) * relevance
    popularity += popularity * gpt_score * random.uniform(0.8, 1.2) * relevance
    print (reputation, likes, popularity)

    bot.likeness = likes
    bot.popularity = popularity
    bot.save()

    return likes

def get_bot_attributes(bot_id=0):
    bot = Bot.objects.get(id=bot_id)
    return bot.likeness, bot.popularity