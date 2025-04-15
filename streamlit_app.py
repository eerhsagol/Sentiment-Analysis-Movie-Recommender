import streamlit as st
import requests
from recommend_movies import recommend

# TMDB API key
API_KEY = 'ead52d23b289bf6952ef430e099374de'

def get_movie_details(movie_title):
    url = f"https://api.themoviedb.org/3/search/movie?query={movie_title}&api_key={API_KEY}"
    response = requests.get(url).json()
    
    if response.get("results"):
        movie = response["results"][0]
        poster_path = movie.get("poster_path")
        poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else None
        summary = movie.get("overview", "No summary available.")
        return poster_url, summary
    return None, "No details found."

# Streamlit page config
st.set_page_config(page_title="MovieMate", page_icon="🎬")

# Custom CSS styles for your new color scheme and input box depth
st.markdown("""
    <style>
        body, .stApp {
            background-color: #FF829B;  /* Soft Pinkish Background */
            font-family: 'Segoe UI', sans-serif;
        }
        .recommend-box {
            background-color: #FFBDBA; /* Soft Pink for recommendation boxes */
            padding: 20px;
            border-radius: 20px;
            color: #2E2E2E;
            margin-bottom: 20px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        }
        .recommend-title {
            font-size: 24px;
            font-weight: bold;
            color: #7D8B67; /* Dark greenish tone for titles */
        }
        .recommend-similarity {
            font-size: 16px;
            color: #5C1A1B;
            margin-bottom: 10px;
        }
        .movie-summary {
            font-size: 14px;
            color: #333333;
        }
        .stTextInput > div > div > input {
            background-color: #7D8B67;
            color: white;
            border-radius: 10px;
            padding: 25px 32px;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2); /* Shadow for depth */
            transition: all 0.3s ease;
            font-size: 16px;  /* Match text size with button */
        }
        .stTextInput > div > div > input:focus {
            box-shadow: 0 0 20px rgba(0, 0, 0, 0.3); /* Focus effect with stronger shadow */
            border: 2px solid #FF1493;  /* Darker pink border on focus */
        }
        .stButton>button {
            background-color: #FF69B4;
            color: white;
            border-radius: 10px;
            padding: 8px 20px;
            font-weight: bold;
            transition: all 0.3s ease;
        }
        .stButton>button:hover {
            background-color: #FF1493;
            color: white;
        }
        .stTextInput > div > div > label {
            color: #FFBDBA; /* Light pink color for input labels */
            opacity: 0.8;  /* Slight transparency for smaller titles */
        }
    </style>
""", unsafe_allow_html=True)

# Title
st.title("🎬 MovieMate")
st.markdown("### Your Personalized Movie Recommendation Buddy")

# Input
movie_input = st.text_input("Enter a movie you liked:")

if st.button("Recommend!"):
    if movie_input:
        recs = recommend(movie_input)

        if recs:
            st.markdown(f"### 🌌 If you liked *'{movie_input}'*, you might also enjoy:")
            for movie, similarity in recs:
                poster_url, summary = get_movie_details(movie)
                html_block = f"""
                <div class="recommend-box">
                    <div class="recommend-title">{movie}</div>
                    <div class="recommend-similarity">🎯 Similarity: {similarity:.2f}%</div>
                    {'<img src="' + poster_url + '" width="200"/><br><br>' if poster_url else ''}
                    <div class="movie-summary">{summary}</div>
                </div>
                """
                st.markdown(html_block, unsafe_allow_html=True)
        else:
            st.warning("Couldn't find any recommendations for that movie.")
    else:
        st.warning("Please enter a movie name.")
