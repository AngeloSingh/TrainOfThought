import os
import json
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TrainOfThought.settings')
django.setup()
from backend.models import Creator, Bot


def flush_database():
    Creator.objects.all().delete()
    Bot.objects.all().delete()


def create_static_records():
    FILE_PATH = 'population_data.json'
    CREATORS_KEY = 'creators'
    ADDITIONAL_USERS = ["User" , "Anonymous"]

    with open(FILE_PATH) as file:
        data = json.load(file)

    for index, user in enumerate(ADDITIONAL_USERS):
        print(index)
        print(user)
        Bot.objects.create(id=index,
    name = user,
    reputation = 0,
    hatred = 0,
    likeness = 0,
    popularity = 0,
    networth = 0,)

    for index, creator_data in enumerate(data[CREATORS_KEY]):
        Creator.objects.create(id = (index+2) , **creator_data)


    for index, creator_data in enumerate(data[CREATORS_KEY]):
        Bot.objects.create(id = (index+2) , name = creator_data['first_name'] + " " + creator_data['last_name'] , reputation = creator_data['default_reputation'] , hatred = creator_data['default_hatred'] , likeness = creator_data['default_popularity'] , popularity = 0 , networth = creator_data['networth'])


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
    flush_database()
    create_static_records()
    get_created_records()