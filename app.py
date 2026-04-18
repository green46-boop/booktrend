import streamlit as st
import pandas as pd
from fetchers import nyt, aladin, kyobo, yes24, uk, japan, germany, goodreads
from classifier import classify
from translator import translate_titles

st.set_page_config(
    page_title="글로벌 논픽션 도서 트렌드",
    page_icon="📚",
    layout="wide",
)

st.title("📚 글로벌 논픽션 도서 트렌드 대시보드")
st.caption("한국 · 미국 · 영국 · 일본 · 독일 베스트셀러 기반")

if st.button("🔄 캐시 초기화 (새로고침)"):
    st.cache_data.clear()
    st.rerun()

st.divider()


def enrich_genre(books):
    for b in books:
        b["genre"] = classify(b["title"], b.get("genre", ""))
    return books


@st.cache_data(ttl=1800)
def load_nyt():
    return enrich_genre(nyt.fetch())

@st.cache_data(ttl=1800)
def load_aladin():
    return enrich_genre(aladin.fetch())

@st.cache_data(ttl=1800)
def load_kyobo():
    return enrich_genre(kyobo.fetch())

@st.cache_data(ttl=1800)
def load_yes24():
    return enrich_genre(yes24.fetch())

@st.cache_data(ttl=1800)
def load_uk():
    books = enrich_genre(uk.fetch())
    titles = [b["title"] for b in books]
    ko_titles = translate_titles(titles)
    for b, kt in zip(books, ko_titles):
        b["ko_title"] = kt
    return books

@st.cache_data(ttl=1800)
def load_japan():
    books = enrich_genre(japan.fetch())
    titles = [b["title"] for b in books]
    ko_titles = translate_titles(titles)
    for b, kt in zip(books, ko_titles):
        b["ko_title"] = kt
    return books

@st.cache_data(ttl=1800)
def load_germany():
    books = enrich_genre(germany.fetch())
    titles = [b["title"] for b in books]
    ko_titles = translate_titles(titles)
    for b, kt in zip(books, ko_titles):
        b["ko_title"] = kt
    return books

@st.cache_data(ttl=1800)
def load_goodreads():
    books = enrich_genre(goodreads.fetch())
    titles = [b["title"] for b in books]
    ko_titles = translate_titles(titles)
    for b, kt in zip(books, ko_titles):
        b["ko_title"] = kt
    return books


def show_books(books, has_ko_title=False):
    if not books:
        st.warning("데이터를 불러오지 못했습니다.")
        return
    df = pd.DataFrame(books)
    cols = ["rank", "title"]
    rename = {"rank": "순위", "title": "원제"}
    if has_ko_title and "ko_title" in df.columns:
        cols.append("ko_title")
        rename["ko_title"] = "가제(한국어)"
    cols += ["author", "genre"]
    rename.update({"author": "저자", "genre": "장르"})
    df = df[cols].rename(columns=rename)
    st.dataframe(df, use_container_width=True, hide_index=True)


# 국가별 베스트셀러
st.header("🌍 국가별 베스트셀러 순위")
tab_kr, tab_us, tab_uk, tab_jp, tab_de = st.tabs(
    ["🇰🇷 한국", "🇺🇸 미국", "🇬🇧 영국", "🇯🇵 일본", "🇩🇪 독일"]
)

with tab_kr:
    sub_aladin, sub_kyobo, sub_yes24 = st.tabs(["알라딘", "교보문고", "Yes24"])
    with sub_aladin:
        with st.spinner("알라딘 로딩 중..."):
            show_books(load_aladin())
    with sub_kyobo:
        st.warning("교보문고는 현재 스크래핑이 불가합니다. (React 기반 사이트)")
    with sub_yes24:
        with st.spinner("Yes24 로딩 중..."):
            show_books(load_yes24())

with tab_us:
    with st.spinner("NYT 로딩 중..."):
        show_books(load_nyt())

with tab_uk:
    with st.spinner("Amazon UK 로딩 중..."):
        show_books(load_uk(), has_ko_title=True)

with tab_jp:
    with st.spinner("Amazon JP 로딩 중..."):
        show_books(load_japan(), has_ko_title=True)

with tab_de:
    with st.spinner("Spiegel 로딩 중..."):
        show_books(load_germany(), has_ko_title=True)

st.divider()

# 크로스오버 시그널
st.header("🔁 크로스오버 시그널")
st.info("Phase 3에서 구현 예정 — 2개국 이상 공통 베스트셀러")

st.divider()

# 장르 온도계
st.header("🌡️ 국가별 장르 온도계")
st.info("Phase 3에서 구현 예정 — 국가별 장르 분포")

st.divider()

# 신흥 시그널
st.header("🌱 신흥 시그널 (Goodreads)")
with st.spinner("Goodreads 로딩 중..."):
    show_books(load_goodreads(), has_ko_title=True)

st.divider()

# 한국 미출간 주목작
st.header("🔍 한국 미출간 해외 주목작")
st.info("Phase 3에서 구현 예정 — 해외 베스트셀러 중 한국 미출간 도서")
