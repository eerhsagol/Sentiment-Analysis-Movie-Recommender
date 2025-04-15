import pandas as pd
import re
import os

def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-z\s]', '', text)
    return text

def clean_comments_csv(input_file, output_dir="data/cleaned"):
    os.makedirs(output_dir, exist_ok=True)
    df = pd.read_csv(input_file)
    cleaned_data = []

    for _, row in df.iterrows():
        movie = row['movie']
        comments = str(row['comments'])
        split_comments = re.split(r'[.!?]\s+', comments)
        cleaned = [clean_text(c) for c in split_comments if c.strip() != ""]
        for comment in cleaned:
            cleaned_data.append({"movie": movie, "comment": comment})

    cleaned_df = pd.DataFrame(cleaned_data)
    output_file = os.path.join(output_dir, "cleaned_comments.csv")
    cleaned_df.to_csv(output_file, index=False)
    print(f"✅ Cleaned comments saved to {output_file}")

if __name__ == "__main__":
    clean_comments_csv("data/reddit_movie_comments.csv")