GENRE_MAP = {
    "경제/경영": [
        "business", "economy", "economic", "finance", "financial", "money",
        "leadership", "management", "marketing", "startup", "invest",
        "경영", "경제", "비즈니스", "투자", "마케팅", "리더십",
        "Wirtschaft", "Finanzen", "keizai", "ビジネス",
    ],
    "역사": [
        "history", "war", "empire", "civilization", "ancient", "medieval",
        "역사", "전쟁", "제국", "문명",
        "Geschichte", "Krieg",
    ],
    "과학": [
        "science", "biology", "physics", "quantum", "brain", "climate",
        "universe", "space", "evolution", "gene", "DNA",
        "과학", "우주", "뇌", "진화",
        "Wissenschaft",
    ],
    "사회/정치": [
        "politics", "political", "democracy", "society", "power", "justice",
        "inequality", "race", "gender", "nation", "government",
        "사회", "정치", "민주주의", "불평등",
        "Politik", "Gesellschaft",
    ],
    "자기계발": [
        "self-help", "habit", "success", "productivity", "mindset",
        "motivation", "goal", "discipline", "atomic",
        "자기계발", "습관", "성공",
        "Ratgeber", "Erfolg",
    ],
    "심리": [
        "psychology", "psycholog", "mind", "behavior", "thinking", "cognitive",
        "emotion", "anxiety", "therapy",
        "심리", "정신", "인지",
        "Psychologie",
    ],
    "전기/회고록": [
        "biography", "memoir", "autobiography", "life of", "story of",
        "자서전", "회고록", "전기",
        "Biografie", "Memoiren",
    ],
    "철학/인문": [
        "philosophy", "philos", "ethics", "moral", "wisdom", "meaning",
        "인문", "철학", "윤리",
        "Philosophie",
    ],
}

DEFAULT_GENRE = "논픽션/기타"


def classify(title: str, existing_genre: str = "") -> str:
    skip = {"", "non-fiction", "nonfiction", "Sachbuch", "ビジネス"}
    if existing_genre and existing_genre not in skip:
        return existing_genre
    title_lower = title.lower()
    for genre, keywords in GENRE_MAP.items():
        if any(kw.lower() in title_lower for kw in keywords):
            return genre
    return DEFAULT_GENRE
