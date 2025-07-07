from flask import Flask, request, jsonify, render_template, send_from_directory
from clustering import load_and_clean_data, apply_kmeans
from youtube_api import search_youtube
import pandas as pd
import os

# Serve static folder normally and serve static React-like frontend under /watch
app = Flask(__name__, static_folder="static", static_url_path="/static")

# ✅ Load and preprocess Netflix data
df, features_scaled = load_and_clean_data("data/netflix_titles.csv")
labels, model = apply_kmeans(features_scaled, n_clusters=6)
df['cluster'] = labels

# ✅ Recommendation logic
def recommend_similar_shows(df, show_title, n_recommendations=5):
    if show_title not in df['title'].values:
        return []
    cluster = df[df['title'] == show_title]['cluster'].values[0]
    recos = df[(df['cluster'] == cluster) & (df['title'] != show_title)]
    return recos[['title', 'genres', 'rating', 'duration']].head(n_recommendations).to_dict(orient='records')

# ✅ Home route (Jinja)
@app.route('/')
def home():
    return render_template("index.html")

# ✅ Watch route (serve static file)
@app.route("/watch")
def serve_watch_static():
    return send_from_directory('static/watch', 'index.html')

# ✅ Static assets under /watch (optional)
@app.route("/watch/<path:filename>")
def serve_watch_static_files(filename):
    return send_from_directory('static/watch', filename)

# ✅ Music search route (Jinja)
@app.route('/music', methods=['GET', 'POST'])
def music():
    videos = []
    query = ""
    if request.method == 'POST':
        query = request.form.get('search')
        if query:
            videos = search_youtube(query)
    return render_template("music.html", videos=videos, query=query)

# ✅ Recommendation API
@app.route('/recommend')
def recommend():
    title = request.args.get('title')
    if not title:
        return jsonify({"error": "Please provide a title using ?title=Your Show Title"}), 400
    result = recommend_similar_shows(df, title)
    if not result:
        return jsonify({"error": f"No recommendations found for '{title}'."}), 404
    return jsonify({"input_title": title, "recommendations": result})

if __name__ == '__main__':
    app.run(debug=True)
