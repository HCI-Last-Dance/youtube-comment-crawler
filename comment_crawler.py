# 댓글 가져오는 코드, 대댓글 안 가져옴

import json
import random
from youtube_comment_downloader import YoutubeCommentDownloader
import re
import os

def generate_random_reactions():
    return {
        "useful": random.randint(0, 100),
        "agree": random.randint(0, 100),
        "curious": random.randint(0, 100),
        "creative": random.randint(0, 100),
        "disagree": random.randint(0, 100),
    }

def assign_tab_and_cluster():
    tab = random.choice(["information", "opinion", "question"])
    cluster = random.choice(["support", "oppose"]) if tab == "opinion" else None
    return tab, cluster

def is_manipulated():
    return random.choices([False, True], weights=[90, 10])[0]

def remove_invisible_prefix(text):
    cleaned = re.sub(r'^[\u200b\u200c\u200d\ufeff\u200e\u200f\u2060\s]+', '', text)
    return cleaned

def crawl_youtube_comments(video_url, max_comments=100):
    downloader = YoutubeCommentDownloader()
    comments_data = []

    for comment in downloader.get_comments_from_url(video_url, sort_by=0):
        text = comment.get("text", "")
        cleaned = remove_invisible_prefix(text).strip()
        if cleaned.startswith("@"):
            continue

        print(f"Processing comment: {comment.get("text", "")[:30]}...")
        
        if len(comments_data) >= max_comments:
            break

        tab, cluster = assign_tab_and_cluster()
        comments_data.append({
            "comment_id": comment.get("cid"),
            "author_id": comment.get("author"),
            "author_name": comment.get("author"),
            "author_profile_image": comment.get("photo"),
            "timestamp": comment.get("time"),
            "content": comment.get("text"),
            "reply_count": 0 if comment.get("replies") == "" else int(comment.get("replies")),
            "reactions": generate_random_reactions(),
            "time_taken_to_write": random.randint(1, 1800), # seconds (1 to 30 minutes)
            "tab": tab,
            "cluster": cluster,
            "manipulated": is_manipulated()
        })

    return comments_data

def save_to_json(data, filepath):
    os.path.dirname(filepath)
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    video_urls = ["https://www.youtube.com/watch?v=fnCY6ysVkAg"] # 여기에 링크 추가해서 쓰기
    for i, video_url in enumerate(video_urls, start=1):
        print(f"Crawling comments for video: ({i}/{len(video_urls)})")
        comments = crawl_youtube_comments(video_url, max_comments=100)
        save_to_json(comments, f"comments_no_replies/{video_url.split('watch?v=')[-1]}.json")
        print(f"{len(comments)}개의 댓글이 저장되었습니다.")
