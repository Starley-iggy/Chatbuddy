import random
import math
import datetime
import json
import os

# Try to import dotenv for reading .env files
try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass

# Basic Chatbot Settings 

BOT_NAME = "ChatBuddy"
PERSONALITY = "friendly"  # "sarcastic", "chill", "energetic"
MEMORY_FILE = "memory.json"

# Load or create persistent memory
if os.path.exists(MEMORY_FILE):
    with open(MEMORY_FILE, "r") as f:
        user_memory = json.load(f)
else:
    user_memory = {}

# Helper Data

greetings = ["hi", "hello", "hey", "yo", "greetings", "sup", "wassup", "fakka"]

jokes = [
    "Why did the computer show up at work late? It had a hard drive!",
    "Why was the math book sad? Too many problems.",
    "I told my computer I needed a break, and it said 'No problem — I'll go to sleep!'",
    "Why don’t scientists trust atoms? Because they make up everything!",
    "Why did the scarecrow get promoted? Because he was outstanding in his field!",
    "Why did the student eat his homework? Because the teacher said it was a piece of cake!",
    "What do you call a fake noodle? An im-pasta!",
    "Why can't you trust stairs? They're always up to something.",
]

facts = [
    "Did you know? The Eiffel Tower can be 15 cm taller during hot days.",
    "Honey never spoils — archaeologists found edible honey in ancient tombs!",
    "Octopuses have three hearts.",
    "Bananas are berries, but strawberries are not.",
    "Humans and giraffes have the same number of neck bones.",
    "Sharks existed before trees.",
    "Your brain generates about 20 watts of electricity — enough to power a light bulb.",
]

last_joke = None

# Functions


def respond_greeting(text):
    for word in text.split():
        if word.lower() in greetings:
            return random.choice([
                f"Hey there! I'm {BOT_NAME}.",
                "Hello! How are you?",
                "Hi! Nice to chat with you.",
            ])
    return None


def do_math(text):
    try:
        expression = text.lower().replace("calculate", "").replace("what is", "").strip()
        result = eval(expression, {"__builtins__": None}, math.__dict__)
        return f"The answer is {result}."
    except Exception:
        return None


def tell_time():
    now = datetime.datetime.now()
    return f"It's {now.strftime('%A, %B %d, %Y %I:%M %p')}."


def save_memory():
    with open(MEMORY_FILE, "w") as f:
        json.dump(user_memory, f)


def remember(text):
    words = text.split()
    if "remember" in words and "name" in words:
        name = words[-1].capitalize()
        user_memory["name"] = name
        save_memory()
        return f"Okay, I’ll remember your name is {name}!"
    return None


def recall(text):
    if "my name" in text and "what" in text:
        name = user_memory.get("name")
        if name:
            return f"Your name is {name}!"
        else:
            return "Hmm, I don’t think you told me your name yet."
    return None


def play_game():
    print("Let's play 'Guess the Number'! I'm thinking of a number between 1 and 10.")
    number = random.randint(1, 10)
    while True:
        guess = input("Your guess: ")
        if not guess.isdigit():
            print("Please enter a number!")
            continue
        guess = int(guess)
        if guess == number:
            print("You got it!  Congratulations!")
            break
        elif guess < number:
            print("Too low! Try again.")
        else:
            print("Too high! Try again.")

def play_rps():
        print("Let's play Rock, Paper, Scissors! Type 'quit' to stop playing.")
        options = ["rock", "paper", "scissors"]
    
        while True:
            user_choice = input("Your choice (rock/paper/scissors): ").lower().strip()
            if user_choice in ["quit", "exit"]:
                print("Thanks for playing! ")
                break
            if user_choice not in options:
                print("Please type rock, paper, or scissors!")
                continue
    
            bot_choice = random.choice(options)
            print(f"{BOT_NAME} chose {bot_choice}!")
    
            if user_choice == bot_choice:
                print("It's a tie! ")
            elif (user_choice == "rock" and bot_choice == "scissors") or \
                 (user_choice == "scissors" and bot_choice == "paper") or \
                 (user_choice == "paper" and bot_choice == "rock"):
                print("You win! ")
            else:
                print("You lose! ")




def get_weather(city="leeuwarden"):
    from math import ceil

    API_KEY = os.getenv("OPENWEATHER_API_KEY", "")

    if not API_KEY: # If no API key is found, return a fake weather response
        fake_weather = random.choice(["sunny", "rainy", "cloudy", "cold", "hot"])
        if "cold" in fake_weather or "rainy" in fake_weather:
            outfit = "You should wear something warm and maybe grab a jacket!"
        elif "hot" in fake_weather:
            outfit = "It’s hot light clothes and maybe some shades."
        else:
            outfit = "Looks nice outside  dress comfortably!"
        return f"Right now it's {fake_weather} in {city}. {outfit}"

    try:
        import requests
        url = (
            f"http://api.openweathermap.org/data/2.5/weather?"
            f"q={city}&appid={API_KEY}&units=metric"
        )
        data = requests.get(url, timeout=5).json()
        if data.get("cod") != 200:
            return f"Couldn't find weather for '{city}'."
        temp = data["main"]["temp"]
        description = data["weather"][0]["description"]
        outfit = (
            "Wear something warm!" if temp < 15 else
            "A T-shirt should be fine!" if temp < 25 else
            "It’s really hot  stay hydrated!"
        )
        return f"The weather in {city.title()} is {description} at {ceil(temp)}°C. {outfit}"
    except Exception as e:
        return f"Sorry, I couldn’t fetch the weather right now. ({e})"


def tell_joke():
    global last_joke
    possible_jokes = [j for j in jokes if j != last_joke]
    new_joke = random.choice(possible_jokes)
    last_joke = new_joke
    return new_joke


def tell_fact():
    return random.choice(facts)


def add_personality(text):
    if PERSONALITY == "sarcastic":
        return f"Oh wow, {text}? Groundbreaking."
    elif PERSONALITY == "chill":
        return f"{text}... yeah, that’s cool, man."
    elif PERSONALITY == "energetic":
        return f"{text}! Let’s gooo!"
    else:
        return text
# Chat Loop
def chat():
    print(f" Hey! I’m {BOT_NAME}. Type 'quit' to exit.")
    while True:
        user_input = input("You: ").lower().strip()

        if user_input in ["quit", "exit", "bye", "have a great day"]:
            print(f"{BOT_NAME}: Bye! Talk to you later! ")
            break

        # Greeting
        response = respond_greeting(user_input)
        if response:
            print(f"{BOT_NAME}: {response}")
            continue

        # Math
        response = do_math(user_input)
        if response:
            print(f"{BOT_NAME}: {response}")
            continue

        # Memory
        response = remember(user_input)
        if response:
            print(f"{BOT_NAME}: {response}")
            continue

        response = recall(user_input)
        if response:
            print(f"{BOT_NAME}: {response}")
            continue

        # Games
        if "rock" in user_input and "paper" in user_input:
            play_rps()
            continue
        elif "rock" in user_input or "scissors" in user_input:
            play_rps()
            continue
        elif "guess" in user_input or "number" in user_input:
            play_game()
            continue
        elif "game" in user_input or "play" in user_input:
            print(f"{BOT_NAME}: You can play 'Guess the Number' or 'Rock Paper Scissors'! Which one?")
            continue


        # Time/date
        if "time" in user_input or "date" in user_input:
            print(f"{BOT_NAME}: {tell_time()}")
            continue

        # Weather
        if "weather" in user_input:
            city = "Leeuwarden"
            words = user_input.split()
            for w in words:
                if w.lower() not in ["what", "is", "the", "weather", "in"]:
                    city = w
            print(f"{BOT_NAME}: {get_weather(city)}")
            continue

        # Jokes/Facts
        if "joke" in user_input or "another joke" in user_input:
            print(f"{BOT_NAME}: {tell_joke()}")
            continue

        if "fact" in user_input or "another fact" in user_input:
            print(f"{BOT_NAME}: {tell_fact()}")
            continue

        # Fallback
        print(f"{BOT_NAME}: {add_personality('Hmm, I’m not sure about that one.')}")

# Running the Chatbot

if __name__ == "__main__":
    chat()
