from django import template
import re

register = template.Library()




@register.filter
def embed_video_url(url):
    # YouTube handling
    youtube_patterns = [
        r'(?:youtube\.com/(?:[^/]+/.+/|(?:v|e(?:mbed)?)/|.*[?&]v=)|youtu\.be/)([^"&?/ ]{11})',
    ]
    
    for pattern in youtube_patterns:
        match = re.search(pattern, url)
        if match:
            video_id = match.group(1)
            return f'https://www.youtube.com/embed/{video_id}'
    
    # Instagram handling
    instagram_pattern = r'(?:instagram.com/(?:p|reel)/([^/]+))'
    match = re.search(instagram_pattern, url)
    if match:
        post_id = match.group(1)
        return f'https://www.instagram.com/p/{post_id}/embed'
    
    # TikTok handling
    tiktok_pattern = r'(?:tiktok\.com/(?:@[^/]+/video|v)/(\d+))'
    match = re.search(tiktok_pattern, url)
    if match:
        video_id = match.group(1)
        return f'https://www.tiktok.com/embed/v2/{video_id}'
    
    return url  # Fallback to original URL if no matches




@register.filter
def split_urls(value):
    urls = [url.strip() for url in value.split(',') if url.strip()]
    print(urls)  # Debugging: Check what URLs are being processed
    return urls