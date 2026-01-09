import os
import re
from googleapiclient.discovery import build
from dotenv import load_dotenv
from .base_scraper import BaseScraper

load_dotenv()

class YoutubeScraper(BaseScraper):
    def __init__(self):
        self.api_key = os.getenv("YOUTUBE_API_KEY")
        self.youtube = None
        if self.api_key:
            self.youtube = build("youtube", "v3", developerKey=self.api_key)

    def get_channel_id(self, channel_url):
        """Resolves a channel URL to a channel ID."""
        if '/channel/' in channel_url:
            return channel_url.split('/channel/')[1].split('/')[0].split('?')[0]
        
        # Handle @handle or /c/ or /user/
        handle = None
        if '@' in channel_url:
            handle = channel_url.split('@')[1].split('/')[0].split('?')[0]
        elif '/c/' in channel_url:
            handle = channel_url.split('/c/')[1].split('/')[0].split('?')[0]
        elif '/user/' in channel_url:
            # This is technically a username, not a handle
            username = channel_url.split('/user/')[1].split('/')[0].split('?')[0]
            request = self.youtube.channels().list(part="id", forUsername=username)
            response = request.execute()
            if response.get("items"):
                return response["items"][0]["id"]
        
        if handle:
            # Try to find by handle (forHandle parameter works with @handle)
            # Note: handle should NOT include the @ symbol for forHandle
            request = self.youtube.channels().list(part="id", forHandle='@' + handle if not handle.startswith('@') else handle)
            response = request.execute()
            if response.get("items"):
                return response["items"][0]["id"]
        
        return None

    def get_video_urls_from_channel(self, channel_id, max_results=50):
        """Fetches all video URLs from a channel's uploads playlist."""
        if not self.youtube:
            return []

        # 1. Get the uploads playlist ID
        channel_request = self.youtube.channels().list(
            part="contentDetails",
            id=channel_id
        )
        channel_response = channel_request.execute()
        
        if not channel_response.get("items"):
            print(f"Error: Channel {channel_id} not found.")
            return []
            
        uploads_playlist_id = channel_response["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]
        
        # 2. Fetch videos from the playlist
        video_urls = []
        next_page_token = None
        
        while True:
            playlist_request = self.youtube.playlistItems().list(
                part="snippet",
                playlistId=uploads_playlist_id,
                maxResults=min(max_results - len(video_urls), 50),
                pageToken=next_page_token
            )
            playlist_response = playlist_request.execute()
            
            for item in playlist_response.get("items", []):
                v_id = item["snippet"]["resourceId"]["videoId"]
                video_urls.append(f"https://www.youtube.com/watch?v={v_id}")
                
            next_page_token = playlist_response.get("nextPageToken")
            if not next_page_token or len(video_urls) >= max_results:
                break
                
        return video_urls

    def search_videos_in_channel(self, channel_id, max_results=50, published_before=None, published_after=None):
        """
        Fetches video URLs from a channel using the search API.
        This allows for filtering by date (RFC 3339 format, e.g. '2023-01-01T00:00:00Z').
        """
        if not self.youtube:
            return []

        video_urls = []
        next_page_token = None
        
        while True:
            search_request = self.youtube.search().list(
                part="id,snippet",
                channelId=channel_id,
                type="video",
                order="date",
                maxResults=min(max_results - len(video_urls), 50),
                pageToken=next_page_token,
                publishedBefore=published_before,
                publishedAfter=published_after
            )
            search_response = search_request.execute()
            
            for item in search_response.get("items", []):
                v_id = item["id"]["videoId"]
                video_urls.append(f"https://www.youtube.com/watch?v={v_id}")
                
            next_page_token = search_response.get("nextPageToken")
            if not next_page_token or len(video_urls) >= max_results:
                break
                
        return video_urls

    def scrape_batch(self, video_urls):
        """
        Fetches metadata for a batch of video URLs efficiently.
        """
        if not self.youtube:
            return []

        # 1. Extract IDs from URLs
        video_ids = []
        url_map = {} # map id back to url
        for url in video_urls:
            v_id = self.extract_video_id(url)
            if v_id:
                video_ids.append(v_id)
                url_map[v_id] = url
        
        results = []
        # 2. Batch fetch in chunks of 50 (YouTube API limit)
        for i in range(0, len(video_ids), 50):
            batch_ids = video_ids[i:i+50]
            try:
                request = self.youtube.videos().list(
                    part="snippet,statistics",
                    id=",".join(batch_ids)
                )
                response = request.execute()
                
                for item in response.get("items", []):
                    v_id = item["id"]
                    snippet = item["snippet"]
                    stats = item.get("statistics", {})
                    
                    results.append({
                        "title": snippet.get("title", ""),
                        "author": snippet.get("channelTitle", ""),
                        "date": snippet.get("publishedAt", ""),
                        "url": url_map.get(v_id),
                        "metadata": {
                            "views": stats.get("viewCount", "0"),
                            "likes": stats.get("likeCount", "0"),
                            "comments": stats.get("commentCount", "0"),
                        }
                    })
            except Exception as e:
                print(f"Error fetching batch metadata: {e}")
                
        return results

    def extract_video_id(self, url):
        """Extracts the video ID from various YouTube URL formats."""
        from urllib.parse import urlparse, parse_qs
        
        parsed_url = urlparse(url)
        if parsed_url.hostname == 'youtu.be':
            return parsed_url.path[1:]
        if parsed_url.hostname in ('www.youtube.com', 'youtube.com'):
            if parsed_url.path == '/watch':
                p = parse_qs(parsed_url.query)
                return p.get('v', [None])[0]
            if parsed_url.path.startswith(('/embed/', '/v/', '/shorts/')):
                return parsed_url.path.split('/')[2]
        
        # Fallback to regex if urllib parsing doesn't catch it
        pattern = r"(?:v=|\/|embed\/|shorts\/)([0-9A-Za-z_-]{11})"
        match = re.search(pattern, url)
        if match:
            return match.group(1)
        return None

    def scrape(self, url):
        if not self.youtube:
            print("Error: YOUTUBE_API_KEY not found in environment variables.")
            return None

        # Check if it's a channel URL or a video URL
        if any(x in url for x in ['/channel/', '/@', '/c/', '/user/']):
            print(f"Detected channel URL: {url}")
            return {"is_channel": True, "url": url}

        video_id = self.extract_video_id(url)
        if not video_id:
            print(f"Error: Could not extract video ID from {url}")
            return None

        try:
            request = self.youtube.videos().list(
                part="snippet,statistics",
                id=video_id
            )
            response = request.execute()

            if not response["items"]:
                print(f"Error: Video not found for ID {video_id}")
                return None

            video_data = response["items"][0]
            snippet = video_data["snippet"]
            stats = video_data.get("statistics", {})

            title = snippet.get("title", "")
            description = snippet.get("description", "")
            author = snippet.get("channelTitle", "")
            date = snippet.get("publishedAt", "")
            tags = snippet.get("tags", [])

            # Statistics
            views = stats.get("viewCount", "N/A")
            likes = stats.get("likeCount", "N/A")
            comments = stats.get("commentCount", "N/A")

            # Combine title and description for the text field
            text_content = f"Title: {title}\n\nDescription:\n{description}"

            return {
            "title": title,
            "author": author,
            "date": date,
            "text": text_content,
            "url": url,
            "metadata": {
                "video_id": video_id,
                "views": views,
                "likes": likes,
                "comments": comments,
                "tags": tags
            }
        }

        except Exception as e:
            print(f"Error scraping YouTube URL {url}: {e}")
            return None
