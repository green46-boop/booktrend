import streamlit as st
import pandas as pd
from fetchers import nyt, aladin, kyobo, yes24, uk, japan, germany, goodreads
from classifier import classify
from translator import translate_titles
from processor import get_crossover, get_genre_stats, get_unpublished_kr

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
    return nyt.fetch()

@st.cache_data(ttl=1800)
def load_aladin():
    return aladin.fetch()

@st.cache_data(ttl=1800)
def load_yes24():
    return yes24.fetch()

@st.cache_data(ttl=1800)
def load_uk():
    books = enrich_genre(uk.fetch())
    ko_titles = translate_titles([b["title"] for b in books])
    for b, kt in zip(books, ko_titles):
        b["ko_title"] = kt
    return books

@st.cache_data(ttl=1800)
def load_japan():
    books = enrich_genre(japan.fetch())
    ko_titles = translate_titles([b["title"] for b in books])
    for b, kt in zip(books, ko_titles):
        b["ko_title"] = kt
    return books

@st.cache_data(ttl=1800)
def load_germany():
    books = enrich_genre(germany.fetch())
    ko_titles = translate_titles([b["title"] for b in books])
    for b, kt in zip(books, ko_titles):
        b["ko_title"] = kt
    return books

@st.cache_data(ttl=1800)
def load_goodreads():
    books = enrich_genre(goodreads.fetch())
    ko_titles = translate_titles([b["title"] for b in books])
    for b, kt in zip(books, ko_titles):
        b["ko_title"] = kt
    return books

@st.cache_data(ttl=1800)
def load_unpublished():
    foreign = (
        [dict(b, source="미국") for b in load_nyt()[:15]] +
        [dict(b, source="영국") for b in load_uk()[:15]] +
        [dict(b, source="독일") for b in load_germany()[:15]]
    )
    return get_unpublished_kr(foreign)


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
    cols.append("author")
    rename["author"] = "저자"
    if "genre" in df.columns and df["genre"].str.strip().any():
        cols.append("genre")
        rename["genre"] = "장르"
    df = df[cols].rename(columns=rename)
    st.dataframe(df, use_container_width=True, hide_index=True)


# ── 국가별 베스트셀러 ──────────────────────────────────────────
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

# ── 크로스오버 시그널 ─────────────────────────────────────────
st.header("🔁 크로스오버 시그널")
st.caption("2개국 이상 베스트셀러에 동시 등장한 도서")

with st.spinner("크로스오버 분석 중..."):
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
        country_str = " · ".join(
            f"{country}({rank}위)" for country, rank in c["countries"].items()
        )
        rows.append({
            "제목": c["title"],
            "저자": c["author"],
            "등장 국가": country_str,
            "국가 수": c["count"],
        })
    df_cross = pd.DataFrame(rows)
    st.dataframe(df_cross, use_container_width=True, hide_index=True)
else:
    st.info("현재 2개국 이상 공통 베스트셀러가 없습니다.")

st.divider()

# ── 국가별 장르 온도계 ────────────────────────────────────────
st.header("🌡️ 국가별 장르 온도계")
st.caption("각 국가 베스트셀러의 장르 분포")

genre_sources = {
    "🇺🇸 미국(NYT)":   load_nyt(),
    "🇰🇷 한국(Yes24)": load_yes24(),
    "🇬🇧 영국":        load_uk(),
    "🇯🇵 일본":        load_japan(),
    "🇩🇪 독일":        load_germany(),
}

genre_cols = st.columns(len(genre_sources))
for col, (label, books) in zip(genre_cols, genre_sources.items()):
    with col:
        st.subheader(label)
        stats = get_genre_stats(books)
        if stats:
            total = sum(stats.values())
            for genre, count in stats.items():
                pct = count / total
                st.write(f"**{genre}** {count}권")
                st.progress(pct)
        else:
            st.caption("장르 정보 없음")

st.divider()

# ── 신흥 시그널 ───────────────────────────────────────────────
st.header("🌱 신흥 시그널 (Goodreads)")
st.caption("Goodreads 논픽션 인기 도서")
with st.spinner("Goodreads 로딩 중..."):
    show_books(load_goodreads(), has_ko_title=True)

st.divider()

# ── 한국 미출간 해외 주목작 ───────────────────────────────────
st.header("🔍 한국 미출간 해외 주목작")
st.caption("미국·영국·독일 베스트셀러 중 알라딘 검색 결과 없는 도서")

with st.spinner("미출간 도서 확인 중... (시간이 걸릴 수 있습니다)"):
    unpublished = load_unpublished()

if unpublished:
    rows = []
    for b in unpublished:
        rows.append({
            "국가": b.get("source", ""),
            "원제": b["title"],
            "가제(한국어)": b.get("ko_title", ""),
            "저자": b.get("author", ""),
            "장르": b.get("genre", ""),
        })
    df_un = pd.DataFrame(rows)
    st.dataframe(df_un, use_container_width=True, hide_index=True)
else:
    st.info("미출간 주목작이 없거나 확인 중입니다.")
