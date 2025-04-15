import praw
import pandas as pd
import time
import os

reddit = praw.Reddit(
    client_id="eQeAeUfhhVuMrzhtlPYRLg",       
    client_secret="ELQAhGWhqRaa3m5xtj_iQ9Kaly1m-g",  
    user_agent="movie_sentiment_bot by Aggressive_Spirit256"
)

movie_list = [
    # 🧠 Sci-Fi / Fantasy
"Interstellar", "Arrival", "Blade Runner 2049", "Dune (2021)", "Everything Everywhere All At Once",
"Her", "Ex Machina", "The Fifth Element", "District 9", "Looper",
"Star Wars: A New Hope", "Star Wars: The Empire Strikes Back", "Star Trek (2009)", "Avatar",
"The Hunger Games", "Ender's Game", "Snowpiercer", "The Martian", "Prometheus", "Annihilation",

# 🧟 Horror / Thriller
"Get Out", "Us", "The Conjuring", "The Babadook", "Hereditary",
"Midsommar", "The Shining", "It Follows", "A Quiet Place", "The Witch",
"Psycho", "The Texas Chain Saw Massacre", "Saw", "Insidious", "Sinister",
"The Ring", "The Grudge", "Candyman (2021)", "Smile", "Talk to Me (2023)",

# 😂 Comedy
"Superbad", "Step Brothers", "The 40-Year-Old Virgin", "Bridesmaids", "Mean Girls",
"Anchorman", "Tropic Thunder", "The Hangover", "Booksmart", "Palm Springs",
"Monty Python and the Holy Grail", "Shaun of the Dead", "The Nice Guys", "Zombieland", "Napoleon Dynamite",
"Clueless", "Crazy Rich Asians", "Game Night", "The Grand Budapest Hotel", "Horrible Bosses",

# ❤️ Romance / Drama
"Pride and Prejudice", "The Notebook", "La La Land", "Titanic", "Eternal Sunshine of the Spotless Mind",
"Call Me by Your Name", "Before Sunrise", "Before Sunset", "Before Midnight", "Atonement",
"Marriage Story", "The Fault in Our Stars", "Silver Linings Playbook", "500 Days of Summer", "Brooklyn",
"The Spectacular Now", "About Time", "Me Before You", "One Day", "The Vow",

# 🎭 Drama
"The Godfather", "The Shawshank Redemption", "Forrest Gump", "Fight Club", "12 Angry Men",
"Schindler's List", "Good Will Hunting", "Whiplash", "The Social Network", "Spotlight",
"The Pursuit of Happyness", "Moonlight", "Manchester by the Sea", "No Country for Old Men", "The Green Mile",
"There Will Be Blood", "Birdman", "Joker", "American Beauty", "Little Women",

# 🍿 Animated
"Spider-Man: Into the Spider-Verse", "Coco", "Up", "Inside Out", "Toy Story 3",
"Shrek", "Zootopia", "Frozen", "The Incredibles", "Ratatouille",
"How to Train Your Dragon", "Kung Fu Panda", "Finding Nemo", "Big Hero 6", "Soul",
"Turning Red", "Puss in Boots: The Last Wish", "Moana", "Tangled", "WALL·E",

# 🌍 International / World Cinema
"Parasite", "Amélie", "Pan's Labyrinth", "Roma", "The Lives of Others",
"Cinema Paradiso", "The Handmaiden", "Oldboy", "Crouching Tiger, Hidden Dragon", "Train to Busan",
"Bicycle Thieves", "Rashomon", "The Intouchables", "The Secret in Their Eyes", "City of God",
"Portrait of a Lady on Fire", "Spirited Away", "Your Name", "I Saw the Devil", "Memories of Murder",

# 🎥 Cult Classics / Indies
"Donnie Darko", "Requiem for a Dream", "The Big Lebowski", "Eraserhead", "Clerks",
"Mulholland Drive", "Eternal Sunshine of the Spotless Mind", "American Psycho", "Fight Club", "The Room",
"Blue Valentine", "Drive", "Moon", "The Lobster", "The Florida Project",
"Lady Bird", "Frances Ha", "The Lighthouse", "Mid90s", "Swiss Army Man",

# 🕵️‍♂️ Crime / Mystery
"Se7en", "Zodiac", "Prisoners", "Gone Girl", "The Girl with the Dragon Tattoo",
"Mystic River", "L.A. Confidential", "The Departed", "Memento", "Wind River",
"The Usual Suspects", "Chinatown", "Knives Out", "Glass Onion", "The Prestige",
"Sherlock Holmes", "Murder on the Orient Express", "Enola Holmes", "Nightcrawler", "The Talented Mr. Ripley"
]

def fetch_reddit_comments(movie_name, limit=50):
    all_comments = []
    try:
        for submission in reddit.subreddit("movies").search(movie_name, limit=limit):
            submission.comments.replace_more(limit=0)
            for comment in submission.comments.list():
                all_comments.append(comment.body)
    except Exception as e:
        print(f"Error fetching {movie_name}: {e}")
    return all_comments

def scrape_all():
    os.makedirs("data", exist_ok=True)
    data = []
    for movie in movie_list:
        print(f"Fetching: {movie}")
        comments = fetch_reddit_comments(movie)
        joined = " ".join(comments)
        data.append({"movie": movie, "comments": joined})
        time.sleep(2)
    df = pd.DataFrame(data)
    df.to_csv("data/reddit_movie_comments.csv", index=False)
    print("✅ Saved to data/reddit_movie_comments.csv")

if __name__ == "__main__":
    scrape_all()
