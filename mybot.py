from dotenv import load_dotenv
from openai import OpenAI
import discord
import os
import random

# Load environment variables from .env file
load_dotenv()
OPENAI_KEY = os.getenv('OPENAI_KEY')
DISCORD_TOKEN = os.getenv('TOKEN')

# Initialize the OpenAI client
openai_client = OpenAI(api_key=OPENAI_KEY)

def call_openai(question):
    completion = openai_client.chat.completions.create(
        model="gpt-4o",
        messages=[
             {
                 "role": "user",
                 "content": f"Respond like a pirate to the following question:  {question}",
            },
        ]
    )
    # Print the response
    response = completion.choices[0].message.content
    print(response)
    return response

def call_dalle(description):
    response = openai_client.images.generate(
        model="dall-e-3",
        prompt=f"Generate a pirate-themed image of: {description}",
        size="1024x1024",
        quality="standard",
        n=1,
    )
    image_url = response.data[0].url
    return image_url

# List of pirate jokes
pirate_jokes = [
    "Why did the pirate go to school? To improve his 'arrr'ithmetic!",
    "What’s a pirate’s favorite letter? Arrr, but they also like the C (sea)!",
    "Why couldn’t the pirate play cards? Because he was always standing on the deck!",
    "How do pirates know that they are pirates? They think, therefore they arrr!",
    "What did the pirate say when he turned 80? Aye matey!",
    "Why did the pirate buy an eye patch? Because he couldn’t afford an iPad!",
    "What’s a pirate’s favorite type of music? Arrr and B!",
    "How much did the pirate pay for his earrings? A buccaneer!",
    "Why was the pirate a great musician? He had perfect pitch (and a hook)!",
    "What do you call a pirate with two eyes and two legs? A rookie!"
]


# Set up discord
intents = discord.Intents.default()
intents.message_content = True  
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

    if message.content.startswith('$question'):
        print(f"Message: {message.content}")                
        message_content = message.content.split("$question")[1]
        print(f"Question: {message_content}")    
        try:
            response = call_openai(message_content)   
            print(f"Assistant: {response}")    
            print("---")
            await message.channel.send(response)
        except Exception as e:
            await message.channel.send("Try again later.")
            print(e)

    if message.content.startswith('$draw'):
        desc = message.content.split('$draw')[1].strip()
        if not desc:
            await message.channel.send("Arrr, ye need to describe what to draw!")
            return
        try:
            url = call_dalle(desc)
            await message.channel.send(url)
        except Exception as e:
            await message.channel.send("Try again later.")
            print(e)

    if message.content.startswith('$joke'):
        joke = random.choice(pirate_jokes)
        await message.channel.send(joke)

client.run(DISCORD_TOKEN)
