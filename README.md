# youtube-comment-crawler

## 설명
- `comment_crawler.py`: 대댓글 없이, 그냥 댓글만 가져옴
- `comment_crawler_youtube_api.py`: 댓글, 대댓글 다 가져옴 (YouTube API 사용) <- 이걸로 사용하세요 !!!
    - 이걸 쓰려면 `YOUTUBE_API_KEY` 환경변수 설정 필요 (.env에 넣기, 발급은 google cloud console에서)
- `divite_tab.py`: 댓글을 tab별로 나누어 저장 (information.json, opinion.json, question.json)

## 실행 방법
1. `requirements.txt`에 있는 패키지 설치
2. `.env` 파일 생성 후, `YOUTUBE_API_KEY` 환경변수 설정
3. `comment_crawler_youtube_api.py`에 video URL 확인 (혹은 추가)
3. `comment_crawler_youtube_api.py` 실행
4. `divite_tab.py` 실행 (이건 댓글을 tab별로 나누어 저장하는 코드)

## 코드 조작
- `comment_crawler_youtube_api.py`의 `__main__` 부분의 `video_urls` 리스트에 영상 URL을 추가해서 사용 가능
- `max_top_comments`: 가져올 댓글의 최대 개수 설정 (기본값: 100)
- 결과는 각각 vidio ID별로 `comments_with_replies` 폴더에 저장됨
    - 즉, video_urls가 10개면 `comments_with_replies` 폴더에 10개의 파일이 생성되는 형식
- `reactions`, `time_taken_to_write`, `tab`, `cluster`, `manipulated` 관련 필드는 무작위에 가깝게 해서 넣어둠
    - `reactions`는 각각 0~100 사이의 정수 (유익해요, 공감해요, 더 알고 싶어요, 독창적이에요, 반대예요)
    - `time_taken_to_write`는 1~1800 사이의 정수 (초 단위, 즉 1초 ~ 30분)
    - `tab`은 information, opinion, question 중 하나를 랜덤으로 선택
    - `cluster`는 tab이 opinion일 때만 support, oppose 중 하나를 랜덤으로 선택
    - `manipulated`는 90%의 확률로 조작X 필드로 추가, 10%의 확률로 조작O 필드로 추가
- `divite_tab.py`는 `comments_with_replies` 폴더에 있는 댓글 파일들을 tab별로 나누어 저장함

## 참고
- 우선 기존의 댓글 분류를 꼼꼼히 하기 위해, 하나의 영상(수능 관련 영상)만을 대상으로 댓글을 가공한 상태입니다.
- 현재 해당 영상은 fnCY6ysVkAg인데, 이 영상의 댓글들을 바탕으로 manual 하게 탭/클러스터 분류를 하고, 더미 댓글을 추가한 결과를 dummy에 저장해두었습니다.
- 이 dummy 댓글들이 사용자 UI에 보여지는 댓글들의 기반이 됩니다.
- `opinion.ts`의 경우, 이 dummy 댓글들 중 의견성 댓글들의 작성 시각이 수정된 것으로, 그래프의 x축이 시간으로 되어있기 때문에, 더 눈에 띄는 그래프를 위해 작성 시각을 임의로 조정한 것입니다.
