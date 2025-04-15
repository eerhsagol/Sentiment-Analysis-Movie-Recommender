import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import normalize
import ast

# Load genre data globally
try:
    genre_df = pd.read_csv("data/movie_genres.csv")
except:
    genre_df = pd.DataFrame(columns=["movie", "genres"])

# Safely convert stringified vectors
def safe_literal_eval(val):
    try:
        return np.array(ast.literal_eval(val))
    except:
        return None

# Average embeddings if multiple rows per movie
def average_embeddings(df):
    df['embedding'] = df['embedding'].apply(safe_literal_eval)
    df = df.dropna(subset=['embedding'])
    movie_groups = df.groupby('movie')['embedding'].apply(lambda x: np.mean(list(x), axis=0))
    return pd.DataFrame({"movie": movie_groups.index, "embedding": movie_groups.values})

# Final recommend function
def recommend(movie_name, top_n=3):
    df = pd.read_csv("data/movie_embeddings.csv")
    movie_embeddings = average_embeddings(df)

    if movie_name not in movie_embeddings['movie'].values:
        print(f"❌ Movie '{movie_name}' not found in the dataset.")
        return []

    input_vector = movie_embeddings[movie_embeddings['movie'] == movie_name]['embedding'].values[0]
    input_vector = np.array(input_vector).reshape(1, -1)

    # Normalize everything
    embed_matrix = np.vstack(movie_embeddings['embedding'].values)
    embed_matrix = normalize(embed_matrix, axis=1)
    input_vector = normalize(input_vector)

    # Cosine similarity
    similarities = cosine_similarity(input_vector, embed_matrix)[0]
    movie_embeddings['similarity'] = similarities

    # Merge genres
    movie_embeddings = pd.merge(movie_embeddings, genre_df, on='movie', how='left')

    # Genre boost
    input_genres = genre_df[genre_df['movie'] == movie_name]['genres'].values
    if len(input_genres) > 0:
        input_genres = input_genres[0].split(', ')
        def genre_score(row):
            if pd.isna(row['genres']):
                return 0
            overlap = len(set(row['genres'].split(', ')).intersection(input_genres))
            return overlap / len(input_genres)
        movie_embeddings['genre_boost'] = movie_embeddings.apply(genre_score, axis=1)
        movie_embeddings['final_score'] = movie_embeddings['similarity'] + 0.15 * movie_embeddings['genre_boost']
    else:
        movie_embeddings['final_score'] = movie_embeddings['similarity']

    # Sort and exclude input movie
    sorted_df = movie_embeddings.sort_values(by='final_score', ascending=False)
    sorted_df = sorted_df[sorted_df['movie'] != movie_name]

    # Display recommendations
    recs = []
    for i, row in sorted_df.head(top_n).iterrows():
        sim_percent = round(row['final_score'] * 100, 2)
        recs.append((row['movie'], sim_percent))

    return recs
