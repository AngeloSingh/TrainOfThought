from openai import OpenAI

def gpt_post_response(post, person="a random celebrity"):
    client = OpenAI()
    # Make a call to chat gpt-4o-mini with the post

    completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": f"You are a user of a social media site like twitter, please respond to the following post by {person} in this format: An array of an int score from -100 to 100 of how 'liked' the post is, and a set of three responses to the post, each limited to below 100 characters each, and in the style of normal but critical users of twitter, being dumb, with bad grammer (no/random capitalisation), and harsh, swearing if necessary. Make the really sassy and rude, unless they agree, then wayy too happy. Grammatical errors etc are okay, but remember the users are degenerates and like things like drama and controversial opinions, along with including a random aspect where opinions may actually be surprisingly liked/disliked at random."},
            {
                "role": "user",
                "content": post
            }
        ]
    )

    print(completion.choices[0].message.content)

    return(completion.choices[0].message.content)

def gpt_bot_comments(name, number):
    client = OpenAI()
    # Make a call to chat gpt-4o-mini with the post

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
