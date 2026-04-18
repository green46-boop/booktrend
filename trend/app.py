import streamlit as st
import pandas as pd
from fetchers import nyt, aladin, yes24, uk, japan, germany, goodreads
from classifier import classify
from translator import translate_titles
from processor import get_crossover, get_genre_stats

st.set_page_config(
    page_title="글로벌 논픽션 도서 트렌드",
    page_icon="📚",
    layout="wide",
)

st.title("📚 글로벌 논픽션 도서 트렌드 대시보드")
st.caption("한국 · 미국 · 영국 · 일본 · 독일 베스트셀러 기반")

with st.sidebar:
    st.header("설정")
    if st.button("🔄 캐시 초기화"):
        st.cache_data.clear()
        st.rerun()
    st.caption("데이터는 30분마다 자동 갱신됩니다.")
    st.divider()
    st.markdown("**데이터 출처**")
    st.markdown("🇰🇷 알라딘 · Yes24\n\n🇺🇸 NYT Books API\n\n🇬🇧 Amazon UK\n\n🇯🇵 Amazon JP\n\n🇩🇪 Spiegel\n\n📚 Goodreads")

st.divider()


# ── 데이터 로더 ────────────────────────────────────────────────

def enrich(books):
    for b in books:
        b["genre"] = classify(b["title"], b.get("genre", ""))
    return books

def add_ko_title(books):
    titles = [b["title"] for b in books]
    ko = translate_titles(titles)
    for b, kt in zip(books, ko):
        b["ko_title"] = kt
    return books

@st.cache_data(ttl=1800, show_spinner=False)
def load_nyt():
    return nyt.fetch()

@st.cache_data(ttl=1800, show_spinner=False)
def load_aladin():
    return aladin.fetch()

@st.cache_data(ttl=1800, show_spinner=False)
def load_yes24():
    return yes24.fetch()

@st.cache_data(ttl=1800, show_spinner=False)
def load_uk():
    return add_ko_title(enrich(uk.fetch()))

@st.cache_data(ttl=1800, show_spinner=False)
def load_japan():
    return add_ko_title(enrich(japan.fetch()))

@st.cache_data(ttl=1800, show_spinner=False)
def load_germany():
    return add_ko_title(enrich(germany.fetch()))

@st.cache_data(ttl=1800, show_spinner=False)
def load_goodreads():
    return add_ko_title(enrich(goodreads.fetch()))


# ── 공통 테이블 렌더러 ─────────────────────────────────────────

def show_books(books, has_ko_title=False):
    if not books:
        st.warning("데이터를 불러오지 못했습니다.")
        return
    df = pd.DataFrame(books)
    cols, rename = ["rank", "title"], {"rank": "순위", "title": "원제"}
    if has_ko_title and "ko_title" in df.columns:
        cols.append("ko_title")
        rename["ko_title"] = "가제(한국어)"
    cols.append("author")
    rename["author"] = "저자"
    if "genre" in df.columns and df["genre"].str.strip().any():
        cols.append("genre")
        rename["genre"] = "장르"
    st.dataframe(df[cols].rename(columns=rename), use_container_width=True, hide_index=True)


# ── 1. 국가별 베스트셀러 ───────────────────────────────────────
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
        st.warning("교보문고는 React 기반 사이트로 현재 스크래핑이 불가합니다.")
    with sub_yes24:
        with st.spinner("Yes24 로딩 중..."):
            show_books(load_yes24())

with tab_us:
    with st.spinner("NYT 로딩 중..."):
        show_books(load_nyt(), has_ko_title=True)

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


# ── 2. 크로스오버 시그널 ──────────────────────────────────────
st.header("🔁 크로스오버 시그널")
st.caption("2개국 이상 베스트셀러에 동시 등장한 도서")

with st.spinner("분석 중..."):
    country_books = {
        "한국(알라딘)": load_aladin(),
        "한국(Yes24)":  load_yes24(),
        "미국":         load_nyt(),
        "영국":         load_uk(),
        "일본":         load_japan(),
        "독일":         load_germany(),
    }
    crossovers = get_crossover(country_books)

if crossovers:
    rows = []
    for c in crossovers:
        badge = "🌐" * c["count"]
        country_str = "  ·  ".join(
            f"{country} {rank}위" for country, rank in c["countries"].items()
        )
        rows.append({
            "": badge,
            "제목": c["title"],
            "저자": c["author"],
            "등장 국가 및 순위": country_str,
            "국가 수": c["count"],
        })
    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
else:
    st.info("현재 2개국 이상 공통 베스트셀러가 없습니다.")

st.divider()


# ── 3. 장르 온도계 ────────────────────────────────────────────
st.header("🌡️ 국가별 장르 온도계")
st.caption("각 국가 베스트셀러의 장르 분포")

genre_sources = {
    "🇺🇸 미국": load_nyt(),
    "🇰🇷 한국": load_yes24(),
    "🇬🇧 영국": load_uk(),
    "🇯🇵 일본": load_japan(),
    "🇩🇪 독일": load_germany(),
}

cols = st.columns(len(genre_sources))
for col, (label, books) in zip(cols, genre_sources.items()):
    with col:
        st.subheader(label)
        stats = get_genre_stats(books)
        if stats:
            df_genre = (
                pd.DataFrame(stats.items(), columns=["장르", "권수"])
                .set_index("장르")
            )
            st.bar_chart(df_genre, horizontal=True, height=300)
        else:
            st.caption("장르 정보 없음")

st.divider()


# ── 4. 신흥 시그널 (Goodreads) ───────────────────────────────
st.header("🌱 신흥 시그널 (Goodreads)")
st.caption("Goodreads 논픽션 인기 도서")
with st.spinner("Goodreads 로딩 중..."):
    show_books(load_goodreads(), has_ko_title=True)
