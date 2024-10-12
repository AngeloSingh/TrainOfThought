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



def get_created_records():

    creators = Creator.objects.all()

    print("\nCreators:")
    for creator in creators:
        print(f"ID: {creator.id}, Name: {creator.first_name} {creator.last_name}, Net Worth: {creator.networth}")



if __name__ == "__main__":
    create_static_records()
    get_created_records()