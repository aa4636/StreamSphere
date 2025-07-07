import pandas as pd
from sklearn.preprocessing import StandardScaler, MultiLabelBinarizer
from sklearn.cluster import KMeans

def load_and_clean_data(filepath):
    df = pd.read_csv(filepath)

    # Drop rows with missing important fields
    df = df.dropna(subset=['duration', 'rating', 'listed_in', 'type'])

    # Filter to include only movies (optional)
    df = df[df['type'] == 'Movie']

    # Keep only durations that are in minutes
    df = df[df['duration'].str.contains('min', na=False)]
    df['duration'] = df['duration'].str.replace(' min', '').astype(int)

    # Convert genres to list
    df['genres'] = df['listed_in'].apply(lambda x: [g.strip() for g in x.split(',')])

    # One-hot encode genres
    mlb = MultiLabelBinarizer()
    genre_encoded = pd.DataFrame(mlb.fit_transform(df['genres']), columns=mlb.classes_, index=df.index)

    # One-hot encode rating
    rating_encoded = pd.get_dummies(df['rating'], dtype=int)

    # Combine all feature columns
    features = pd.concat([genre_encoded, rating_encoded, df[['duration']]], axis=1)

    # Drop any rows with NaNs in the combined feature set
    features_clean = features.dropna()

    # ⚠️ Filter the original df to match cleaned features index
    df_cleaned = df.loc[features_clean.index].reset_index(drop=True)

    # Normalize features
    scaler = StandardScaler()
    features_scaled = scaler.fit_transform(features_clean)

    return df_cleaned, features_scaled

def apply_kmeans(features_scaled, n_clusters=6):
    model = KMeans(n_clusters=n_clusters, random_state=42)
    labels = model.fit_predict(features_scaled)
    return labels, model
