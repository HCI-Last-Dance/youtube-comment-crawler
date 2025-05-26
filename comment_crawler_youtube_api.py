# 댓글 가져오는 코드, 대댓글까지 가져옴 (YouTube Data API v3 사용)

import requests
import json
import random
import time
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("YOUTUBE_API_KEY")

def generate_random_reactions():
    """랜덤한 반응 점수 생성 (0~100 사이의 정수)"""
    return {
        "useful": random.randint(0, 100), # 유익해요
        "agree": random.randint(0, 100), # 공감해요
        "curious": random.randint(0, 100), # 더 알고 싶어요
        "creative": random.randint(0, 100), # 독창적이에요
        "disagree": random.randint(0, 100), # 반대예요
    }

def assign_tab_and_cluster():
    """tab은 information, opinion, question 중 하나를 랜덤으로 선택, cluster는 opinion일 때만 support, oppose 중 하나를 랜덤으로 선택"""
    tab = random.choice(["information", "opinion", "question"]) # 정보, 의견, 질문
    cluster = random.choice(["support", "oppose"]) if tab == "opinion" else None # 찬성, 반대 (추가 및 변경 가능)
    return tab, cluster

def is_manipulated():
    """90%의 확률로 조작X 필드로 추가, 10%의 확률로 조작O 필드로 추가"""
    return random.choices([False, True], weights=[90, 10])[0]

def get_video_id_from_url(url):
    """영상 ID 추출"""
    if "v=" in url:
        return url.split("v=")[-1].split("&")[0]
    else:
        raise ValueError("Invalid YouTube video URL")

def get_top_level_comments(video_id, max_results=100):
    """영상의 상위 댓글 가져오기"""
    url = "https://www.googleapis.com/youtube/v3/commentThreads"
    params = {
        "part": "snippet",
        "videoId": video_id,
        "maxResults": max_results,
        "order": "relevance",
        "textFormat": "plainText",
        "key": API_KEY
    }

    comments = []
    while len(comments) < max_results:
        response = requests.get(url, params=params).json()
        for item in response.get("items", []):
            c = item["snippet"]["topLevelComment"]["snippet"]
            comment_id = item["snippet"]["topLevelComment"]["id"]
            tab, cluster = assign_tab_and_cluster()

            comment = {
                "comment_id": comment_id,
                "author_id": c.get("authorChannelId", {}).get("value", ""),
                "author_name": c.get("authorDisplayName"),
                "author_profile_image": c.get("authorProfileImageUrl"),
                "timestamp": c.get("publishedAt"),
                "content": c.get("textDisplay"),
                "reactions": generate_random_reactions(),
                "time_taken_to_write": random.randint(1, 1800), # 초 단위 (1초 ~ 30분)
                "tab": tab,
                "cluster": cluster,
                "manipulated": is_manipulated(),
                "reply_ids": [],
                "replies": []
            }

            comments.append(comment)

            if len(comments) >= max_results:
                break

        if "nextPageToken" in response:
            params["pageToken"] = response["nextPageToken"]
            time.sleep(1)
        else:
            break

    return comments

def get_replies(parent_comment_id):
    """댓글에 대한 대댓글 가져오기"""
    url = "https://www.googleapis.com/youtube/v3/comments"
    params = {
        "part": "snippet",
        "parentId": parent_comment_id,
        "maxResults": 100,
        "textFormat": "plainText",
        "key": API_KEY
    }

    replies = []
    response = requests.get(url, params=params).json()
    for item in response.get("items", []):
        r = item["snippet"]
        reply = {
            "comment_id": item["id"],
            "author_id": r.get("authorChannelId", {}).get("value", ""),
            "author_name": r.get("authorDisplayName"),
            "author_profile_image": r.get("authorProfileImageUrl"),
            "timestamp": r.get("publishedAt"),
            "content": r.get("textDisplay"),
            "reactions": generate_random_reactions(),
            "time_taken_to_write": random.randint(1, 1800), # 초 단위 (1초 ~ 30분)
            "manipulated": is_manipulated()
        }
        replies.append(reply)
    return replies

def crawl_comments(video_url, max_top_comments=100):
    """댓글, 대댓글 크롤링"""
    video_id = get_video_id_from_url(video_url)
    print(f"[INFO] Fetching top-level comments for video: {video_id}")

    comments = get_top_level_comments(video_id, max_results=max_top_comments)

    for comment in comments:
        replies = get_replies(comment["comment_id"])
        comment["reply_ids"] = [r["comment_id"] for r in replies]
        comment["replies"] = replies
        print(f" → {comment['content'][:30]}... ({len(replies)} replies)")

    return comments

def save_to_json(data, filepath):
    """JSON 파일로 저장"""
    os.path.dirname(filepath)
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    video_urls = [ # 여기에 링크 추가해서 쓰기
        "https://www.youtube.com/watch?v=fnCY6ysVkAg", # 수능 2번
        "https://www.youtube.com/watch?v=vSqoBPWy074", # 댕댕이 식당 동반
        "https://www.youtube.com/watch?v=FAbMP0m57tM", # 뉴진스
        "https://www.youtube.com/watch?v=Bd-DEHwbyhI", # 대학 축제 연예인
        "https://www.youtube.com/watch?v=AeUx8ltLhlI", # 지브리
        "https://www.youtube.com/watch?v=e2jmfTpjG18", # 프랑스 결선투표제
        "https://www.youtube.com/watch?v=f1aaiQCTAP8", # 청년 백수
        "https://www.youtube.com/watch?v=7bdoq_zUvEs", # 칸예
        "https://www.youtube.com/watch?v=UKI9h5dJ_T4" # 스마트기기
    ]
    
    for i, video_url in enumerate(video_urls, start=1):
        print(f"[INFO] Crawling comments for video: ({i}/{len(video_urls)}) {video_url}")
        comments = crawl_comments(video_url, max_top_comments=100)
        save_to_json(comments, f"comments_with_replies/{get_video_id_from_url(video_url)}.json")
        print(f"[DONE] Saved {len(comments)} top-level comments with replies.")

