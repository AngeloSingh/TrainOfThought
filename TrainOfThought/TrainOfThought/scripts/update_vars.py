import random
from backend.models import Bot  # Adjust the import according to your project structure

def update_attributes(bot_id, gpt_score, relevance):
    bot = Bot.objects.get(id=bot_id)
    reputation = bot.reputation
    likes = bot.likeness
    reposts = bot.popularity  # Assuming you want to update popularity as reposts

    popularity = 0.95 - (0.9 - reputation)
    likes += popularity * gpt_score * random.uniform(0.8, 1.2) * relevance
    reposts += popularity * gpt_score * random.uniform(0.8, 1.2) * relevance

    bot.likeness = likes
    bot.popularity = reposts
    bot.save()

    return likes, reposts

def get_bot_attributes(bot_id=0):
    bot = Bot.objects.get(id=bot_id)
    return bot.likeness, bot.popularity