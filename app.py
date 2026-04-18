import streamlit as st
import pandas as pd
from fetchers import nyt, aladin, kyobo, yes24, uk, japan, germany, goodreads

st.set_page_config(
    page_title="글로벌 논픽션 도서 트렌드",
    page_icon="📚",
    layout="wide",
)

st.title("📚 글로벌 논픽션 도서 트렌드 대시보드")
st.caption("한국 · 미국 · 영국 · 일본 · 독일 베스트셀러 기반")

st.divider()


def show_books(books, empty_msg="데이터를 불러오지 못했습니다."):
    if not books:
        st.warning(empty_msg)
        return
    df = pd.DataFrame(books)[["rank", "title", "author"]].rename(
        columns={"rank": "순위", "title": "제목", "author": "저자"}
    )
    st.dataframe(df, use_container_width=True, hide_index=True)


@st.cache_data(ttl=1800)
def load_nyt():
    return nyt.fetch()

@st.cache_data(ttl=1800)
def load_aladin():
    return aladin.fetch()

@st.cache_data(ttl=1800)
def load_kyobo():
    return kyobo.fetch()

@st.cache_data(ttl=1800)
def load_yes24():
    return yes24.fetch()

@st.cache_data(ttl=1800)
def load_uk():
    return uk.fetch()

@st.cache_data(ttl=1800)
def load_japan():
    return japan.fetch()

@st.cache_data(ttl=1800)
def load_germany():
    return germany.fetch()

@st.cache_data(ttl=1800)
def load_goodreads():
    return goodreads.fetch()


# 국가별 베스트셀러
st.header("🌍 국가별 베스트셀러 순위")
tab_kr, tab_us, tab_uk, tab_jp, tab_de = st.tabs(
    ["🇰🇷 한국", "🇺🇸 미국", "🇬🇧 영국", "🇯🇵 일본", "🇩🇪 독일"]
)

with tab_kr:
    sub_aladin, sub_kyobo, sub_yes24 = st.tabs(["알라딘", "교보문고", "Yes24"])
    with sub_aladin:
        with st.spinner("알라딘 데이터 로딩 중..."):
            show_books(load_aladin())
    with sub_kyobo:
        with st.spinner("교보문고 데이터 로딩 중..."):
            show_books(load_kyobo())
    with sub_yes24:
        with st.spinner("Yes24 데이터 로딩 중..."):
            show_books(load_yes24())

with tab_us:
    with st.spinner("NYT 데이터 로딩 중..."):
        show_books(load_nyt())

with tab_uk:
    with st.spinner("Waterstones 데이터 로딩 중..."):
        show_books(load_uk())

with tab_jp:
    with st.spinner("honto 데이터 로딩 중..."):
        show_books(load_japan())

with tab_de:
    with st.spinner("Spiegel 데이터 로딩 중..."):
        show_books(load_germany())

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
with st.spinner("Goodreads 데이터 로딩 중..."):
    gr_books = load_goodreads()
    if gr_books:
        df = pd.DataFrame(gr_books)
        cols = ["rank", "title", "author"]
        if "rating" in df.columns:
            cols.append("rating")
        df = df[cols].rename(columns={
            "rank": "순위", "title": "제목", "author": "저자", "rating": "평점"
        })
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.warning("데이터를 불러오지 못했습니다.")

st.divider()

# 한국 미출간 주목작
st.header("🔍 한국 미출간 해외 주목작")
st.info("Phase 3에서 구현 예정 — 해외 베스트셀러 중 한국 미출간 도서")
