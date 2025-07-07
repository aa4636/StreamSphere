from flask import Flask, request, jsonify, render_template, send_from_directory
from clustering import load_and_clean_data, apply_kmeans
from youtube_api import search_youtube
import pandas as pd
import os 

# ✅ Initialize Flask and serve React frontend from 'watch/' folder
app = Flask(__name__, static_folder="static/watch", static_url_path="/watch")

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

# ✅ Home route
@app.route('/')
def home():
    return render_template("index.html")

# ✅ Serve React OTT UI from /watch
@app.route("/watch")
def serve_watch():
    return send_from_directory(app.static_folder, "index.html")

@app.route("/watch/<path:path>")
def serve_watch_assets(path):
    return send_from_directory(app.static_folder, path)

# ✅ Music search route (YouTube streaming mode)
@app.route('/music', methods=['GET', 'POST'])
def music():
    videos = []
    query = ""
    if request.method == 'POST':
        query = request.form.get('search')
        if query:
            videos = search_youtube(query)
    return render_template("music.html", videos=videos, query=query)

# ✅ Recommendation API endpoint (used for frontend integration)
@app.route('/recommend')
def recommend():
    title = request.args.get('title')
    if not title:
        return jsonify({"error": "Please provide a title using ?title=Your Show Title"}), 400
    result = recommend_similar_shows(df, title)
    if not result:
        return jsonify({"error": f"No recommendations found for '{title}'."}), 404
    return jsonify({"input_title": title, "recommendations": result})

# ✅ Run the app
if __name__ == '__main__':
    app.run(debug=True)


#from flask import Flask, request, jsonify, render_template
#from clustering import load_and_clean_data, apply_kmeans
#from flask import send_from_directory

# Initialize Flask app
#app = Flask(__name__, static_folder="watch", static_url_path="/watch")

# Step 1: Load and preprocess the data
#df, features_scaled = load_and_clean_data("data/netflix_titles.csv")

# Step 2: Apply KMeans clustering
#labels, model = apply_kmeans(features_scaled, n_clusters=6)

# Step 3: Add cluster labels to dataframe
#df['cluster'] = labels

# Step 4: View cluster summary
#print("Cluster sizes:")
#print(df['cluster'].value_counts())

# Step 5: Preview shows from one cluster
#print("\nSample shows from cluster 2:")
#print(df[df['cluster'] == 2][['title', 'genres', 'duration', 'rating']].head())

#def recommend_similar_shows(df, show_title, n_recommendations=5):
    # Check if the show exists
    #if show_title not in df['title'].values:
       #return [] #f"Show '{show_title}' not found in dataset."

    # Get cluster label of the selected show
    #cluster = df[df['title'] == show_title]['cluster'].values[0]

    # Filter shows in the same cluster (excluding the input show)
    #similar_shows = df[(df['cluster'] == show_cluster) & (df['title'] != show_title)]

    # Get top N recommendations
    #recos = df[(df['cluster'] == cluster) & (df['title'] != show_title)]

    #return recos[['title', 'genres', 'rating', 'duration']].head(n_recommendations).to_dict(orient='records')

#print("\n🎯 Recommendations:")

#title_input = "The Irishman"  # Replace with any title from the dataset
#recommendations = recommend_similar_shows(df, title_input)

#print(recommendations)

#  Homepage Route
#@app.route('/')
#def home():
    #return render_template("index.html")

#adding watch route in app.py
#@app.route("/watch")
#def serve_watch():
    #return send_from_directory(app.static_folder, "index.html")

#@app.route("/watch/<path:path>")
#def serve_watch_assets(path):
    #return send_from_directory(app.static_folder, path)

#music mode with api key
#from youtube_api import search_youtube

#@app.route('/music', methods=['GET', 'POST'])
#def music():
    #videos = []
    #query = ""
    #if request.method == 'POST':
        #query = request.form.get('search')
        #if query:
            #videos = search_youtube(query)

    #return render_template("music.html", videos=videos, query=query)

#  Recommend API (used later or in frontend)
#@app.route('/recommend')
#def recommend():
    #title = request.args.get('title')
    #if not title:
        #return jsonify({"error": "Please provide a title using ?title=Your Show Title"}), 400
    #result = recommend_similar_shows(df, title)
    #if not result:
        #return jsonify({"error": f"No recommendations found for '{title}'."}), 404
    #return jsonify({"input_title": title, "recommendations": result})

#if __name__ == '__main__':
    #app.run(debug=True)



