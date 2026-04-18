# 글로벌 논픽션 도서 트렌드 대시보드

## 개발 페이즈

### Phase 1 — 기반 세팅
- `requirements.txt` 작성 (streamlit, requests, beautifulsoup4, pandas)
- `config.py` 작성 (NYT API 키 등 설정값)
- `fetchers/` 디렉토리 및 `__init__.py` 생성
- Streamlit 앱 뼈대(`app.py`) 생성 및 로컬 실행 확인

### Phase 2 — 데이터 수집 (fetchers)
각 fetcher는 `[{"rank", "title", "author", "genre", "isbn", "source"}]` 형태의 리스트를 반환
- `nyt.py` — NYT Books API (논픽션 3개 리스트)
- `aladin.py` — 알라딘 베스트셀러 스크래핑
- `kyobo.py` — 교보문고 베스트셀러 스크래핑
- `yes24.py` — Yes24 베스트셀러 스크래핑
- `uk.py` — Waterstones 스크래핑
- `japan.py` — honto.jp 스크래핑
- `germany.py` — Spiegel Bestseller 스크래핑
- `goodreads.py` — Goodreads 논픽션 shelf 스크래핑

### Phase 3 — 데이터 처리 (processor.py)
- 크로스오버 감지: 제목 정규화 후 2개국 이상 등장 도서 추출
- 장르 분류: NYT 카테고리 / 알라딘 카테고리 / 키워드 기반 분류
- 미출간 판별: 해외 베스트셀러를 알라딘에서 검색, 결과 없으면 미출간

### Phase 4 — 대시보드 UI (app.py)
- 국가별 베스트셀러 탭 (한국 탭 내 알라딘·교보·Yes24 서브탭)
- 크로스오버 시그널 섹션
- 국가별 장르 온도계 (가로 막대 차트)
- Goodreads 신흥 시그널 섹션
- 한국 미출간 해외 주목작 섹션

### Phase 5 — 마무리
- 스크래핑 실패 시 에러 없이 "데이터 없음" 처리
- `st.cache_data(ttl=1800)` 캐싱 적용
- UI 레이아웃·색상 다듬기
- GitHub push 및 최종 정리

---

## 프로젝트 목적
5개국(한국, 미국, 영국, 일본, 독일) 논픽션 베스트셀러 데이터를 수집·분석해 트렌드를 한눈에 파악하는 대시보드.
초보 개발자가 로컬에서 혼자 사용하는 도구이며 로그인 없음.

## 기술 스택
- **Streamlit** — 대시보드 UI (`streamlit run app.py`로 실행)
- **requests + BeautifulSoup** — 해외 사이트 스크래핑
- **pandas** — 데이터 가공
- **st.cache_data(ttl=1800)** — 30분 캐싱으로 API/스크래핑 부하 방지

## 실행 방법
```bash
pip install streamlit requests beautifulsoup4 pandas
streamlit run app.py
```

## 데이터 소스

| 국가 | 출처 | 방식 |
|------|------|------|
| 미국 | NYT Books API | API |
| 한국 | 알라딘 + 교보문고 + Yes24 | 스크래핑 |
| 영국 | Waterstones | 스크래핑 |
| 일본 | honto.jp | 스크래핑 |
| 독일 | Spiegel Bestseller | 스크래핑 |
| Goodreads | goodreads.com/shelf/show/non-fiction | 스크래핑 |

## API 키 설정 (`config.py`)
- `NYT_API_KEY` — 이미 발급됨 (`nyt_bestsellers.py` 참고)
- 한국 3개 서점(알라딘, 교보, Yes24)은 모두 스크래핑으로 수집, 별도 API 키 불필요

## 디렉토리 구조
```
booktrend/
├── nyt_bestsellers.py     (초기 NYT 테스트 스크립트, 건드리지 않음)
├── app.py                 (Streamlit 메인 앱)
├── config.py              (API 키 등 설정값)
├── processor.py           (크로스오버 감지, 장르 분석, 미출간 판별)
├── fetchers/
│   ├── __init__.py
│   ├── nyt.py             (미국 - NYT API)
│   ├── aladin.py          (한국 - 알라딘 스크래핑)
│   ├── kyobo.py           (한국 - 교보문고 스크래핑)
│   ├── yes24.py           (한국 - Yes24 스크래핑)
│   ├── uk.py              (영국 - Waterstones 스크래핑)
│   ├── japan.py           (일본 - honto.jp 스크래핑)
│   ├── germany.py         (독일 - Spiegel 스크래핑)
│   └── goodreads.py       (Goodreads 스크래핑)
└── requirements.txt
```

## 대시보드 섹션

### 1. 국가별 베스트셀러 순위
- 탭: 한국 / 미국 / 영국 / 일본 / 독일
- 한국 탭: 알라딘·교보·Yes24 서브탭으로 구분 (모두 스크래핑), 세 곳 공통 등장 시 "트리플 차트인" 배지
- 공통 데이터 구조: `{"rank", "title", "author", "genre", "isbn", "source"}`

### 2. 크로스오버 시그널
- 2개국 이상 동시 등장 도서를 자동 감지
- 제목 정규화(소문자, 특수문자 제거) 후 비교
- 등장 국가 수가 많을수록 강조 표시

### 3. 국가별 장르 온도계
- 각 국가 베스트셀러의 장르 분포를 가로 막대로 시각화
- NYT: 리스트 카테고리 활용 / 알라딘: categoryId / 기타: 키워드 분류

### 4. 신흥 시그널 (Goodreads)
- Goodreads 논픽션 인기 도서 목록
- 각 책의 한국 출간 여부 표시 (알라딘 검색 기반)

### 5. 한국 미출간 해외 주목작
- 미국·영국·일본·독일 베스트셀러를 알라딘에서 제목으로 검색 (스크래핑)
- 결과 없으면 "미출간"으로 분류, 국가별 그룹화 표시
