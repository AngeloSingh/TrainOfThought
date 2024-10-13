from openai import OpenAI
from dotenv import load_dotenv
import os
import sqlite3
import json
import random

def gpt_post_response(post, person="a random celebrity"):
    # Load environment variables from .env file
    load_dotenv()

    # Get the API key from the environment variable
    api_key = os.getenv("OPENAI_API_KEY")

    # Initialize the OpenAI client with the API key
    client = OpenAI(api_key=api_key)
    # Make a call to chat gpt-4o-mini with the post

    completion = client.chat.completions.create(
    model="gpt-4o-mini-2024-07-18",
    messages=[
        {"role": "system", "content": f"You are a brainrotted, braindead user of a social media site like twitter, please respond to the following post by {person} (take into account general public opinion of this person) in this format: An array of an int score from -100 to 100 of how 'liked' the post is (for controversial posts, it can be strongly either way regardless of the sentiment of the post). This should be gotten from the generated comments, which are a set of three responses to the post, each limited to below 100 characters each, and in the style of normal but critical users of twitter, being dumb, with bad grammer (no/random capitalisation), and harsh, swearing if necessary. Each comment is in an array with a 'sentiment' score, i.e positive the comment is, or how sarcastic it is. 100 means very strongly positive, -100 means very negative. Make the really sassy and rude, unless they agree, then wayy too happy. Grammatical errors etc are okay, but remember the users are degenerates and like things like drama and controversial opinions, along with including a random aspect where opinions may actually be surprisingly liked/disliked at random. So the output should be in the format: [50, ['I agree with this', 60], ['I disagree with this', 20], ['This is the worst thing I have ever seen', 100]]"},
            {
                "role": "user",
                "content": post
            }
        ]
    )

    response_content = completion.choices[0].message.content

    try:
        response_array = eval(response_content)
        score = response_array[0]
        comments = response_array[1:]
        comments = [[comment, sentiment] for comment, sentiment in comments]
    except (SyntaxError, IndexError, ValueError) as e:
        print(f"Error parsing response: {e}")
        score = None
        comments = []

    return([score, comments])

def gpt_bot_comments(name, number):
    # Load environment variables from .env file
    load_dotenv()

    # Get the API key from the environment variable
    api_key = os.getenv("OPENAI_API_KEY")

    # Initialize the OpenAI client with the API key
    client = OpenAI(api_key=api_key)

    completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": f"You are a user of a social media site like twitter (the name will be provided by the user) please randomly create {number} tweets on any random topics (each can be different) for that user, though be aggressive and dumb like an actual twitter user, sharing 'hot takes', etc. If the name is specific, include those thoughts within the tweets where possible, i.e Political, a specific 'Stan' account, etc. Be below 100 characters in each tweet, and return them as an array of strings."},
        {
                "role": "user",
                "content": "Name: " + name
            }
        ]
    )
    
    # Parse the message content to get the array of strings
    tweets = completion.choices[0].message.content.strip().split('\n')

    print(tweets)
    
    return tweets

# Ask chatgpt to general 100 random twitter posts (under 75 characters each)
def gpt_random_tweets(bot):
    # Load environment variables from .env file
    load_dotenv()

    # Get the API key from the environment variable
    api_key = os.getenv("OPENAI_API_KEY")

    # Initialize the OpenAI client with the API key
    client = OpenAI(api_key=api_key)

    completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": f"You are a user of a social media site like twitter, specifically the celebrity {bot['name']}, please randomly create 10 tweets them (each can be about different topics connected to them), though all must be related directly to and something the people would actually tweet, including their strong opinions, and controvercial takes, though be aggressive and dumb like an actual twitter user, sharing 'hot takes', etc. They have a reputation of {bot['reputation']} / 100, and are liked by {bot['likeness']}% of the population, so adjust the insanity of the tweets accordingly. Again, the tweets should be unique to the person and their beliefs, good or bad. Be below 75 characters in each tweet, and return them as an array of strings."}
    ]
    )

    # Extract the JSON array from the response content
    try:
        response_content = completion.choices[0].message.content
        start_index = response_content.find('[')
        end_index = response_content.rfind(']') + 1
        tweets_json = response_content[start_index:end_index]
        tweets = json.loads(tweets_json)
    except (json.JSONDecodeError, ValueError) as e:
        print(f"Error parsing tweets: {e}")
        tweets = []

    print(tweets)

    return tweets

# Create main function to generate the bot with id 1's tweets
# Retrieve the bot info from the sqlite file in the above directory


def main():
    # Connect to the SQLite database
    db_path = "../../db.sqlite3"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    #cursor.execute("SELECT name, reputation, likeness FROM backend_bot WHERE id = 1")
    #bot_info = cursor.fetchone()
    bot_info = True

    if bot_info:
        bot = {
            "name": "Ryan Reynolds",
            "reputation": 0,
            "likeness": 0
        }

        # Generate tweets for the bot
        tweets = gpt_random_tweets(bot)
        
        # Save to database in table backend_post
        for tweet in tweets:
            # Calculate likes and reposts based on reputation and likeness
            max_value = 20000
            likes = min(int(bot['reputation'] / 100 * max_value), max_value)
            reposts = min(int(bot['likeness'] / 100 * max_value), max_value)

            # Randomly adjust likes and reposts to be mostly between 0 and 1000
            likes = random.randint(0, min(likes, 1000))
            reposts = random.randint(0, min(reposts, 1000))

            cursor.execute(
            "INSERT INTO backend_post (bot_id, content, likes, reposts) VALUES (?, ?, ?, ?)",
            (1, tweet, likes, reposts)
            )
            conn.commit()
    else:
        print("Bot with id 1 not found.")

    # Close the database connection
    conn.close()


if __name__ == "__main__":
    main()