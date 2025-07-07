from googleapiclient.discovery import build

# REPLACE with your actual YouTube API key
YOUTUBE_API_KEY = "AIzaSyCLH7gsfaccpJ32ZmSRdwKpoEqeT4QuIK0"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

# Initialize YouTube API client
youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=YOUTUBE_API_KEY)

def search_youtube(query, max_results=11):
    """
    Search for embeddable videos on YouTube.
    Returns top video + 10 recommendations.
    """
    search_response = youtube.search().list(
        q=query,
        type="video",
        part="id,snippet",
        videoEmbeddable="true",  # ✅ Ensures videos can be embedded
        maxResults=max_results
    ).execute()

    results = []
    for item in search_response['items']:
        video_id = item['id']['videoId']
        title = item['snippet']['title']
        results.append({
            "title": title,
            "video_id": video_id
        })

    return results
