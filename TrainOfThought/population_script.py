import os
import json
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TrainOfThought.settings')
django.setup()
from backend.models import Creator, Bot

def create_static_records():
    FILE_PATH = 'population_data.json'
    CREATORS_KEY = 'creators'

    with open(FILE_PATH) as file:
        data = json.load(file)


    for creator_data in data[CREATORS_KEY]:
        Creator.objects.create(**creator_data)


def create_user_bot():
    Bot.objects.create(id = 0, name="User", reputation=0, hatred=0, likeness=0, popularity=0, networth=0)


def get_created_records():

    creators = Creator.objects.all()
    bots = Bot.objects.all()

    print("\nCreators:")
    for creator in creators:
        print(f"ID: {creator.id}, Name: {creator.first_name} {creator.last_name}, Net Worth: {creator.networth}")

    print("\nBots:")
    for bot in bots:
        print(f"ID: {bot.id}, Name: {bot.name}, Net Worth: {bot.networth}")


if __name__ == "__main__":
    create_static_records()
    create_user_bot()
    get_created_records()