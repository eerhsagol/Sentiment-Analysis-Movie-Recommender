import pandas as pd
from sentence_transformers import SentenceTransformer
import time

model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

def generate_embeddings(input_csv="data/cleaned/cleaned_comments.csv", output_csv="data/movie_embeddings.csv", max_total_comments=100000):
    df = pd.read_csv(input_csv)
    df = df.dropna(subset=['comment'])
    df['comment'] = df['comment'].astype(str)

    # Get number of movies
    unique_movies = df['movie'].unique()
    comments_per_movie = max_total_comments // len(unique_movies)

    # Sample evenly across movies
    balanced_df = df.groupby('movie').apply(lambda x: x.sample(n=min(comments_per_movie, len(x)), random_state=42)).reset_index(drop=True)

    print(f"🔢 Total comments being embedded: {len(balanced_df)}")

    embeddings = []
    for i, comment in enumerate(balanced_df['comment']):
        try:
            emb = model.encode(comment)
            embeddings.append(emb.tolist())
        except Exception as e:
            print(f"⚠️ Skipping row {i} due to error: {e}")
            embeddings.append([0.0]*384)

        if i % 100 == 0:
            print(f"✅ {i}/{len(balanced_df)} comments embedded...")
            time.sleep(0.5)

    balanced_df['embedding'] = embeddings
    balanced_df.to_csv(output_csv, index=False)
    print(f"✅ Done. {len(balanced_df)} embeddings saved to {output_csv}")

if __name__ == "__main__":
    generate_embeddings()
