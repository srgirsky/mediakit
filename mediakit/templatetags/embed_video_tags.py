from django import template
import re

register = template.Library()




@register.filter
def embed_video_url(url):
    if 'youtube.com' in url:
        # Extract the video ID from the YouTube URL
        match = re.search(r'v=([^&]+)', url)
        if match:
            video_id = match.group(1)
            return f'https://www.youtube.com/embed/{video_id}'
    elif 'youtu.be' in url:
        # Handle shortened YouTube URLs
        match = re.search(r'youtu\.be/([^?]+)', url)
        if match:
            video_id = match.group(1)
            return f'https://www.youtube.com/embed/{video_id}'
    # Add more conditions for other platforms if needed
    return url  # Fallback to the original URL




@register.filter
def split_urls(value):
    urls = [url.strip() for url in value.split(',') if url.strip()]
    print(urls)  # Debugging: Check what URLs are being processed
    return urls