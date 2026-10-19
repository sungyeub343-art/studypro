from datetime import datetime
from html import escape
import json
from pathlib import Path
import re
import xml.etree.ElementTree as ET
from zoneinfo import ZoneInfo


ROOT = Path(__file__).resolve().parents[1]
SITE_URL = "https://studypro.kr"
SEOUL_TIMEZONE = ZoneInfo("Asia/Seoul")
SOCIAL_IMAGE_URL = f"{SITE_URL}/og-image-20261009.png"
SOCIAL_IMAGE_ALT = "대구 수학과외 - 이해가 성적이 되는 1:1 맞춤 수업"

DISTRICTS = {
    "jung-gu": ("중구", [
        "동인동", "삼덕동", "성내1동", "성내2동", "성내3동", "대신동",
        "남산1동", "남산2동", "남산3동", "남산4동", "대봉1동", "대봉2동",
    ]),
    "dong-gu": ("동구", [
        "신암1동", "신암2동", "신암3동", "신암4동", "신암5동", "신천1·2동",
        "신천3동", "신천4동", "효목1동", "효목2동", "도평동", "불로봉무동",
        "지저동", "동촌동", "방촌동", "해안동", "안심1동", "안심2동",
        "안심3동", "안심4동", "혁신동", "공산동",
    ]),
    "seo-gu": ("서구", [
        "내당1동", "내당2·3동", "내당4동", "비산1동", "비산2·3동", "비산4동",
        "비산5동", "비산6동", "비산7동", "평리1동", "평리2동", "평리3동",
        "평리4동", "평리5동", "평리6동", "상중이동", "원대동",
    ]),
    "nam-gu": ("남구", [
        "이천동", "봉덕1동", "봉덕2동", "봉덕3동", "대명1동", "대명2동",
        "대명3동", "대명4동", "대명5동", "대명6동", "대명9동", "대명10동", "대명11동",
    ]),
    "buk-gu": ("북구", [
        "고성동", "칠성동", "침산1동", "침산2동", "침산3동", "노원동",
        "산격1동", "산격2동", "산격3동", "산격4동", "복현1동", "복현2동",
        "대현동", "검단동", "무태조야동", "관문동", "태전1동", "태전2동",
        "구암동", "관음동", "읍내동", "동천동", "국우동",
    ]),
    "suseong-gu": ("수성구", [
        "범어1동", "범어2동", "범어3동", "범어4동", "만촌1동", "만촌2동",
        "만촌3동", "수성1가동", "수성2·3가동", "수성4가동", "황금1동", "황금2동",
        "중동", "상동", "파동", "두산동", "지산1동", "지산2동", "범물1동",
        "범물2동", "고산1동", "고산2동", "고산3동",
    ]),
    "dalseo-gu": ("달서구", [
        "성당동", "두류1·2동", "두류3동", "본리동", "감삼동", "죽전동", "장기동",
        "용산1동", "용산2동", "이곡1동", "이곡2동", "신당동", "월성1동", "월성2동",
        "진천동", "유천동", "상인1동", "상인2동", "상인3동", "도원동", "송현1동",
        "송현2동", "본동",
    ]),
    "dalseong-gun": ("달성군", [
        "화원읍", "논공읍", "다사읍", "유가읍", "옥포읍", "현풍읍", "가창면", "하빈면", "구지면",
    ]),
    "gunwi-gun": ("군위군", [
        "군위읍", "소보면", "효령면", "부계면", "우보면", "의흥면", "산성면", "삼국유사면",
    ]),
}

REPRESENTATIVE_AREAS = {
    "jung-gu": "동인동·삼덕동·대봉동·남산동",
    "dong-gu": "신암동·효목동·안심동·혁신동",
    "seo-gu": "내당동·비산동·평리동·원대동",
    "nam-gu": "대명동·봉덕동·이천동",
    "buk-gu": "침산동·산격동·복현동·동천동",
    "suseong-gu": "범어동·만촌동·수성동·황금동",
    "dalseo-gu": "상인동·월성동·진천동·용산동",
    "dalseong-gun": "화원읍·다사읍·유가읍·현풍읍",
    "gunwi-gun": "군위읍·효령면·부계면·우보면",
}

# 학년별 키워드 페이지: 지역명 + 학년 + (수학수업·수학공부·기초수학·수학내신·수능대비·수능수학)
GRADES = {
    "elementary": {
        "name": "초등",
        "eyebrow": "ELEMENTARY MATH",
        "title_tail": "초등 수학수업·수학공부·기초수학",
        "tagline": "기초가 단단해지는 수업",
        "description": "{place} 초등 수학과외 - 초등 수학수업, 초등 수학공부 습관, 초등 기초수학을 1:1로 지도합니다. 초1~초6 연산·서술형부터 예비중1 준비까지 학생 수준에 맞춰 설계합니다.",
        "intro": "{short} 초등학생의 연산 정확도와 교과 개념, 문장제 해석력을 1:1로 점검하고 스스로 공부하는 습관까지 함께 만듭니다.",
        "summary": "초등 수학수업에서 연산과 교과 개념을 다지고, 스스로 하는 초등 수학공부 습관과 기초수학을 함께 잡습니다.",
        "lesson_heading": "초등 수학,<br>이렇게 수업합니다",
        "lesson_text": "초등 수학은 정답보다 생각하는 과정이 중요합니다. 학생이 개념을 자기 말로 설명할 수 있을 때까지 확인하고, 연산 실수와 서술형 풀이 습관을 함께 바로잡습니다.",
        "cards": [
            ("LESSON", "초등 수학수업", "교과서 개념을 학생이 직접 설명할 수 있을 때까지 1:1로 확인하고, 연산 정확도와 문장제 해석을 함께 다집니다."),
            ("STUDY HABIT", "초등 수학공부 습관", "수업마다 숙제 분량과 복습 주기를 정해 혼자 공부하는 시간을 만들고, 틀린 문제는 풀이 과정부터 다시 점검합니다."),
            ("FOUNDATION", "초등 기초수학", "수 감각과 사칙연산, 분수·소수처럼 다음 학년으로 이어지는 기초 개념의 빈틈을 먼저 찾아 채웁니다."),
        ],
        "stages": [
            ("초등 저학년 수학과외", "초1~초3 수 개념과 덧셈·뺄셈, 곱셈구구, 길이와 시각처럼 생활 속 수학을 그림과 구체물로 익힙니다."),
            ("초등 고학년 수학과외", "초4~초6 분수와 소수, 비와 비율, 도형의 넓이 등 중등 수학의 바탕이 되는 단원을 깊이 있게 다집니다."),
            ("예비중1 수학과외", "정수와 유리수, 문자와 식을 미리 익혀 중학교 수학을 자신감 있게 시작하도록 준비합니다."),
        ],
        "faqs": [
            ("초등학생도 1:1 수학과외가 필요할까요?", "초등 시기에는 연산 습관과 개념 이해의 작은 빈틈이 중등 수학에서 크게 벌어집니다. 1:1 수업은 학생이 어디서 막히는지 바로 확인하고 그 자리에서 바로잡을 수 있습니다."),
            ("수학 기초가 많이 부족해도 시작할 수 있나요?", "가능합니다. 첫 수업에서 이전 학년 개념까지 진단한 뒤, 필요한 단원으로 돌아가 기초수학부터 다시 쌓고 현재 학년 진도와 연결합니다."),
            ("초등 수학 선행은 어느 정도 하나요?", "현재 학년 개념이 충분히 안정된 경우에만 선행 범위를 정합니다. 무리한 선행보다 서술형과 응용 문제까지 이해하는 것을 우선합니다."),
        ],
    },
    "middle": {
        "name": "중등",
        "eyebrow": "MIDDLE SCHOOL MATH",
        "title_tail": "중등 수학내신·수학공부·기초수학",
        "tagline": "내신과 개념을 함께 잡는 수업",
        "description": "{place} 중등 수학과외 - 중1·중2·중3 중등 수학내신 대비와 중등 수학수업, 수학공부 방법, 기초수학 보완까지 1:1 맞춤으로 준비합니다.",
        "intro": "{short} 중학생의 학교 진도와 시험 범위를 기준으로 개념, 유형, 서술형을 1:1로 준비하고 흔들리는 기초까지 함께 보완합니다.",
        "summary": "중등 수학수업과 학교별 수학내신 대비, 흔들리는 기초수학 보완까지 중학생의 수학공부 흐름을 설계합니다.",
        "lesson_heading": "중등 수학,<br>이렇게 수업합니다",
        "lesson_text": "중학교 수학은 단원끼리 연결되어 있어 한 번 놓친 개념이 다음 학년까지 이어집니다. 현재 진도와 이전 개념을 함께 점검하고, 학교 시험에 맞춘 내신 대비를 진행합니다.",
        "cards": [
            ("LESSON", "중등 수학수업", "학교 진도에 맞춰 개념 설명, 대표 유형, 변형 문제 순서로 1:1 수업을 진행합니다."),
            ("STUDY HABIT", "중등 수학공부 방법", "개념 노트와 오답 노트를 함께 관리해 시험 직전이 아니라 평소에 실력이 쌓이도록 공부 흐름을 잡습니다."),
            ("FOUNDATION", "중등 기초수학", "분수 연산부터 일차방정식까지 막힌 지점으로 돌아가 중학 수학의 기초를 다시 세웁니다."),
            ("SCHOOL EXAM", "중등 수학내신", "학교별 시험 범위와 출제 경향, 서술형 비중을 반영해 내신 대비 일정을 세웁니다."),
        ],
        "stages": [
            ("중1 수학과외", "정수와 유리수, 일차방정식, 좌표평면과 그래프 등 중학교 수학의 첫 단원을 정확하게 익힙니다."),
            ("중2 수학과외", "연립방정식과 일차함수, 도형의 성질처럼 내신 변별력이 높은 단원을 유형별로 준비합니다."),
            ("중3 수학과외", "인수분해와 이차방정식, 이차함수를 다지며 예비고1 공통수학으로 자연스럽게 연결합니다."),
        ],
        "faqs": [
            ("중등 수학내신 기간에는 어떻게 수업하나요?", "시험 4~5주 전부터 학교 교과서와 부교재, 기출 유형을 기준으로 범위를 정리하고 서술형 답안 작성까지 연습합니다."),
            ("수학 기초가 부족한 중학생도 따라갈 수 있나요?", "진단을 통해 초등·중등 과정 중 비어 있는 개념을 찾고, 현재 진도와 병행하며 기초수학을 단계적으로 보완합니다."),
            ("중3은 언제부터 고등 수학을 준비하면 좋을까요?", "중3 내신이 안정되면 2학기부터 공통수학의 다항식과 방정식 단원을 중심으로 고등 수학 준비를 시작하는 것을 권합니다."),
        ],
    },
    "high": {
        "name": "고등",
        "eyebrow": "HIGH SCHOOL MATH",
        "title_tail": "수능수학·수능대비·수학내신",
        "tagline": "내신부터 수능까지 이어지는 수업",
        "description": "{place} 고등 수학과외 - 고등 수학내신, 수능대비, 수능수학을 1:1로 준비합니다. 고1 공통수학부터 고3 수능 기출까지 고등 기초수학 점검과 함께 설계합니다.",
        "intro": "{short} 고등학생의 내신 일정과 모의고사, 수능 목표를 함께 고려해 개념, 기출, 실전 문제를 단계적으로 1:1 지도합니다.",
        "summary": "고등 수학내신과 수능대비를 함께 준비합니다. 기초수학 점검부터 수능수학 실전 연습까지 단계별로 수업합니다.",
        "lesson_heading": "고등 수학,<br>이렇게 수업합니다",
        "lesson_text": "고등 수학은 학습량이 많아 우선순위가 중요합니다. 내신 시험과 모의고사 일정을 기준으로 개념, 기출, 실전 연습의 비중을 학생별로 조정합니다.",
        "cards": [
            ("LESSON", "고등 수학수업", "개념의 원리부터 고난도 문항 접근법까지 학생 수준에 맞춰 1:1로 수업합니다."),
            ("STUDY PLAN", "고등 수학공부 계획", "내신과 모의고사 일정을 기준으로 주간 학습량을 정하고, 복습 여부를 매 수업 점검합니다."),
            ("FOUNDATION", "고등 기초수학", "중학 수학의 빈틈 때문에 고등 개념이 막힌다면 필요한 단원부터 다시 연결합니다."),
            ("SCHOOL EXAM", "고등 수학내신", "학교별 기출과 부교재, 수행평가 일정을 반영해 내신 등급 목표에 맞춰 준비합니다."),
            ("CSAT PREP", "고등 수능대비", "평가원 기출을 분석하고 단원별 취약 유형을 정리해 실전 시간 배분까지 연습합니다."),
            ("CSAT MATH", "고등 수능수학", "목표 등급에 따라 기본 문항의 정확도와 고난도 문항 접근 비중을 조정합니다."),
        ],
        "stages": [
            ("고1 수학과외", "공통수학1·2의 개념과 학습량에 적응하고, 고등학교 첫 내신 시험을 안정적으로 준비합니다."),
            ("고2 수학과외", "대수, 미적분Ⅰ, 확률과 통계 등 과목별 내신과 모의고사를 함께 대비합니다."),
            ("고3 수학과외", "수능 기출과 실전 모의고사로 취약 단원을 보완하고 목표 등급에 맞춘 문제 풀이 전략을 세웁니다."),
        ],
        "faqs": [
            ("고등 수학내신과 수능대비를 동시에 할 수 있나요?", "가능합니다. 시험 기간에는 내신 비중을 높이고, 시험이 끝나면 수능 기출과 모의고사 분석으로 전환하는 방식으로 일정을 조정합니다."),
            ("수학 기초가 부족한 고등학생도 수업이 가능한가요?", "진단 후 고등 개념에 필요한 중학 수학 단원부터 빠르게 정리하고, 현재 학교 진도와 병행하며 고등 기초수학을 보완합니다."),
            ("수능수학은 언제부터 준비하면 좋을까요?", "고1·고2는 내신 개념을 탄탄히 하면서 모의고사로 수능 유형에 익숙해지고, 고3은 기출 분석과 실전 연습 비중을 높이는 것을 권합니다."),
        ],
    },
}

EXPECTED_PAGE_COUNT = 150
EXPECTED_GRADE_PAGE_COUNT = (len(DISTRICTS) + 1) * len(GRADES)
GENERATED_START = "<!-- LOCALITY-LINKS:START -->"
GENERATED_END = "<!-- LOCALITY-LINKS:END -->"
SEO_HEAD_START = "<!-- SEO-HEAD:START -->"
SEO_HEAD_END = "<!-- SEO-HEAD:END -->"
PHONE_BUTTON = '<a class="area-phone" href="tel:01029283614" aria-label="010-2928-3614로 전화 상담">전화 상담 <strong>010-2928-3614</strong></a>'
FONT_LINKS = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Gowun+Batang:wght@700&family=Noto+Sans+KR:wght@400;500;600;700;800&display=swap" rel="stylesheet">'


def json_ld(data: object) -> str:
    text = json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    return f'<script type="application/ld+json">{text}</script>'


def breadcrumb_ld(items: list[tuple[str, str]]) -> dict:
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": position, "name": name, "item": url}
            for position, (name, url) in enumerate(items, 1)
        ],
    }


def faq_ld(faqs: list[tuple[str, str]]) -> dict:
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": question, "acceptedAnswer": {"@type": "Answer", "text": answer}}
            for question, answer in faqs
        ],
    }


def organization_ld(name: str, url: str, area: str) -> dict:
    return {
        "@context": "https://schema.org",
        "@type": "EducationalOrganization",
        "name": name,
        "url": url,
        "telephone": "+82-10-2928-3614",
        "areaServed": {"@type": "Place", "name": area},
    }


def social_meta(title: str, description: str, canonical: str) -> str:
    return (
        f'<meta name="theme-color" content="#173b35"><meta property="og:type" content="website"><meta property="og:locale" content="ko_KR">'
        f'<meta property="og:title" content="{escape(title)}"><meta property="og:description" content="{escape(description)}"><meta property="og:url" content="{canonical}">\n'
        f'  <meta property="og:site_name" content="STUDY PRO">\n'
        f'  <meta property="og:image" content="{SOCIAL_IMAGE_URL}">\n'
        f'  <meta property="og:image:secure_url" content="{SOCIAL_IMAGE_URL}">\n'
        f'  <meta property="og:image:type" content="image/png">\n'
        f'  <meta property="og:image:width" content="1200">\n'
        f'  <meta property="og:image:height" content="630">\n'
        f'  <meta property="og:image:alt" content="{SOCIAL_IMAGE_ALT}">\n'
        f'  <meta name="twitter:card" content="summary_large_image">\n'
        f'  <meta name="twitter:title" content="{escape(title)}">\n'
        f'  <meta name="twitter:description" content="{escape(description)}">\n'
        f'  <meta name="twitter:image" content="{SOCIAL_IMAGE_URL}">\n'
        f'  <meta name="twitter:image:alt" content="{SOCIAL_IMAGE_ALT}">'
    )


def grade_cards(area_label: str, href_prefix: str) -> str:
    cards = []
    for grade_slug, grade in GRADES.items():
        href = f"{href_prefix}{grade_slug}/"
        cards.append(
            f'<article class="transition-card grade-card reveal"><small>{grade["eyebrow"]}</small>'
            f'<h3><a href="{href}">{escape(area_label)} {grade["name"]} 수학과외</a></h3>'
            f'<p>{escape(grade["summary"])}</p><a class="grade-more" href="{href}">{grade["name"]} 수업 자세히 보기 <span aria-hidden="true">↗</span></a></article>'
        )
    return "".join(cards)


def grade_section(area_label: str, href_prefix: str, intro: str) -> str:
    return (
        f'<section class="area-guide section grade-program" id="grades"><div class="area-guide-header reveal"><div><p class="eyebrow">GRADE PROGRAM</p>'
        f'<h2>{escape(area_label)} 학년별<br>수학과외 안내</h2></div><p>{escape(intro)}</p></div>'
        f'<div class="transition-grid">{grade_cards(area_label, href_prefix)}</div></section>'
    )


def locality_kind(locality: str) -> str:
    if locality.endswith("읍"):
        return "읍"
    if locality.endswith("면"):
        return "면"
    return "동"


def locality_links(localities: list[str], current_index: int | None = None) -> str:
    links = []
    for index, locality in enumerate(localities, 1):
        current = ' aria-current="page"' if index == current_index else ""
        links.append(
            f'<a href="../locality-{index:02d}/"{current}>{escape(locality)} <span aria-hidden="true">↗</span></a>'
        )
    return "".join(links)


def parent_links_block(district_name: str, localities: list[str]) -> str:
    links = "".join(
        f'<a href="locality-{index:02d}/">{escape(locality)} <span aria-hidden="true">↗</span></a>'
        for index, locality in enumerate(localities, 1)
    )
    grades = grade_section(
        district_name,
        "",
        f"{district_name} 초등·중등·고등 학생의 학년과 목표에 맞춰 수업을 설계합니다. 초등 기초수학부터 중등 수학내신, 고등 수능수학까지 학년별 안내를 확인하세요.",
    )
    faq_items = "".join(
        f'<details{" open" if index == 0 else ""}><summary>{escape(question)}<span aria-hidden="true">+</span></summary><p>{escape(answer)}</p></details>'
        for index, (question, answer) in enumerate(DISTRICT_FAQS)
    )
    return (
        f'{GENERATED_START}\n'
        f'    {grades}\n'
        f'    <section class="area-care section" id="care"><div class="area-care-heading reveal">'
        f'<div><p class="eyebrow">PERSONAL CARE SYSTEM</p><h2>{escape(district_name)} 학생을 위한<br>빈틈없는 1:1 관리</h2></div>'
        f'<p>수업 시간에 이해하는 것에서 끝나지 않습니다. 진단부터 주간 복습까지 이어지는 관리로 혼자서도 풀 수 있는 힘을 만듭니다.</p></div>'
        f'<div class="area-care-summary reveal"><div><strong>1:1</strong><span>학생별 맞춤 수업</span></div>'
        f'<div><strong>초·중·고</strong><span>학년별 목표 설계</span></div><div><strong>4 STEP</strong><span>진단부터 복습까지</span></div></div>'
        f'<div class="area-care-grid">'
        f'<article class="reveal"><small>STEP 01</small><span aria-hidden="true">01</span><h3>현재 위치 진단</h3><p>단원별 이해도와 풀이 습관을 확인해 먼저 채워야 할 빈틈을 찾습니다.</p></article>'
        f'<article class="reveal"><small>STEP 02</small><span aria-hidden="true">02</span><h3>맞춤 진도 설계</h3><p>학교 일정과 목표 점수를 반영해 개념, 유형, 심화의 순서를 정합니다.</p></article>'
        f'<article class="reveal"><small>STEP 03</small><span aria-hidden="true">03</span><h3>설명하는 수업</h3><p>학생이 풀이 근거를 직접 말하고 쓰며 배운 개념을 자기 것으로 만듭니다.</p></article>'
        f'<article class="reveal"><small>STEP 04</small><span aria-hidden="true">04</span><h3>복습·오답 관리</h3><p>반복되는 실수와 취약 유형을 기록하고 다음 수업에서 다시 점검합니다.</p></article>'
        f'</div></section>\n'
        f'    <section class="localities section" id="localities"><p class="eyebrow">{escape(district_name)} LOCAL AREA</p>'
        f'<h2>{escape(district_name)} 동·읍·면 수학과외</h2><p class="localities-intro">거주 지역을 선택하면 가까운 곳에서 진행하는 1:1 맞춤 수업을 확인할 수 있습니다.</p>'
        f'<div class="locality-links">{links}</div></section>\n'
        f'    <section class="area-faq section"><div class="area-faq-heading reveal"><p class="eyebrow">FREQUENTLY ASKED</p>'
        f'<h2>{escape(district_name)} 수학과외<br>자주 묻는 질문</h2><p>수업 시작 전에 궁금한 내용을 확인해 보세요.</p></div>'
        f'<div class="area-faq-list reveal">{faq_items}</div></section>\n'
        f'    <section class="area-cta"><div class="area-cta-inner reveal"><div><p class="eyebrow light">START TOGETHER</p>'
        f'<h2>{escape(district_name)}에서 시작하는<br>학생 맞춤 수학 수업</h2><p>현재 고민과 목표를 들려주시면 필요한 학습 방향부터 함께 정리해 드립니다.</p></div>'
        f'<div class="area-cta-actions"><a href="../#contact">무료 학습 상담 <span aria-hidden="true">↗</span></a>'
        f'<a href="tel:01029283614"><small>전화 상담</small><strong>010-2928-3614</strong></a></div></div></section>\n'
        f'    {GENERATED_END}\n'
    )


DISTRICT_FAQS = [
    ("수업은 어떤 방식으로 진행되나요?", "학생의 현재 실력과 목표를 먼저 확인한 뒤 1:1로 개념 설명, 문제 적용, 오답 정리를 진행합니다."),
    ("초등·중등·고등 모두 수업이 가능한가요?", "초등 기초수학과 수학공부 습관, 중등 수학내신, 고등 내신과 수능수학까지 학년별 목표에 맞춰 수업합니다."),
    ("내신과 선행 학습을 함께 할 수 있나요?", "학교 시험 일정과 이해도를 기준으로 내신 대비를 우선하고, 학습 여유에 맞춰 다음 과정의 선행 범위를 조정합니다."),
    ("상담할 때 무엇을 알려야 하나요?", "학생의 학년, 최근 성적, 어려워하는 단원, 원하는 목표를 알려주시면 더 구체적으로 안내해 드릴 수 있습니다."),
]


def parent_head(district_slug: str, district_name: str) -> tuple[str, str, str]:
    canonical = f"{SITE_URL}/{district_slug}/"
    title = f"대구 {district_name} 수학과외 | 초등·중등·고등 수학 1:1 맞춤 수업"
    description = (
        f"대구 {district_name} 수학과외 - {REPRESENTATIVE_AREAS[district_slug]} 초등 기초수학, 중등 수학내신, "
        "고등 수능수학까지 1:1 맞춤 수업. 학생의 현재 실력을 진단하고 학년별 수학공부 방향을 설계합니다."
    )
    structured = "".join(json_ld(data) for data in (
        organization_ld(f"대구 {district_name} 수학과외", canonical, f"대구광역시 {district_name}"),
        breadcrumb_ld([("대구 수학과외", f"{SITE_URL}/"), (f"{district_name} 수학과외", canonical)]),
        faq_ld(DISTRICT_FAQS),
    ))
    block = (
        f'{SEO_HEAD_START}\n'
        f'  <meta name="description" content="{escape(description)}">\n'
        f'  {social_meta(title, description, canonical)}\n'
        f'  <link rel="canonical" href="{canonical}"><title>{escape(title)}</title>\n'
        f'  {structured}\n'
        f'  {SEO_HEAD_END}'
    )
    return block, title, description


def update_parent_head(text: str, district_slug: str, district_name: str, path: Path) -> str:
    block, _, _ = parent_head(district_slug, district_name)
    if SEO_HEAD_START in text:
        return re.sub(
            rf"{re.escape(SEO_HEAD_START)}.*?{re.escape(SEO_HEAD_END)}",
            lambda _: block,
            text,
            count=1,
            flags=re.S,
        )
    # 최초 1회: 손으로 작성된 메타 태그를 걷어내고 생성 블록으로 교체
    head_end = text.index("</head>")
    head, rest = text[:head_end], text[head_end:]
    for pattern in (
        r'<meta name="description"[^>]*>',
        r'<meta name="theme-color"[^>]*>',
        r'<meta property="og:[^"]+"[^>]*>',
        r'<meta name="twitter:[^"]+"[^>]*>',
        r'<link rel="canonical"[^>]*>',
        r'<title>.*?</title>',
    ):
        head = re.sub(pattern, "", head, flags=re.S)
    head = re.sub(r"\n[ \t]*(?=\n)", "", head)
    if "<title>" in head:
        raise ValueError(f"Could not replace head tags in {path}")
    return head.rstrip() + f"\n  {block}\n" + rest


def update_parent(district_slug: str, district_name: str, localities: list[str]) -> None:
    path = ROOT / district_slug / "index.html"
    text = path.read_text(encoding="utf-8")
    text = update_parent_head(text, district_slug, district_name, path)
    text = re.sub(r'<a class="area-phone".*?</a>', "", text)
    text, phone_button_count = re.subn(
        r'(<section class="area-hero".*?<div class="area-hero-content">.*?</p>)(</div>\s*</section>)',
        lambda match: f"{match.group(1)}{PHONE_BUTTON}{match.group(2)}",
        text,
        count=1,
        flags=re.S,
    )
    if phone_button_count != 1:
        raise ValueError(f"Area hero not found in {path}")
    text = re.sub(
        rf"\s*{re.escape(GENERATED_START)}.*?{re.escape(GENERATED_END)}\s*",
        "\n",
        text,
        flags=re.S,
    )
    marker = '<section class="nearby section" id="nearby">'
    if marker not in text:
        raise ValueError(f"Nearby section not found in {path}")
    text = text.replace(marker, parent_links_block(district_name, localities) + marker, 1)
    path.write_text(text, encoding="utf-8", newline="\n")


def render_page(district_slug: str, district_name: str, locality: str, index: int, localities: list[str]) -> str:
    canonical = f"{SITE_URL}/{district_slug}/locality-{index:02d}/"
    kind = locality_kind(locality)
    title = f"대구 {district_name} {locality} 수학과외 | 초등·중등·고등 수학 1:1 맞춤"
    description = (
        f"대구 {district_name} {locality} 수학과외 - 초등 기초수학, 중등 수학내신, 고등 수능수학까지 "
        f"{locality} 학생의 실력을 진단하고 학년별 1:1 맞춤 수업으로 준비합니다."
    )
    place_phrase = {"동": "생활권", "읍": "통학 환경", "면": "지역과 통학 일정"}[kind]
    nearby = locality_links(localities, index)
    structured = "".join(json_ld(data) for data in (
        organization_ld(f"대구 {district_name} {locality} 수학과외", canonical, f"대구광역시 {district_name} {locality}"),
        breadcrumb_ld([
            ("대구 수학과외", f"{SITE_URL}/"),
            (f"{district_name} 수학과외", f"{SITE_URL}/{district_slug}/"),
            (f"{locality} 수학과외", canonical),
        ]),
    ))
    grades = grade_section(
        locality,
        "../",
        f"{locality} 초등·중등·고등 학생은 학년마다 필요한 수업이 다릅니다. 초등 수학공부 습관, 중등 수학내신, 고등 수능대비까지 학년별 수업 안내를 확인하세요.",
    )
    return f'''<!doctype html>
<html lang="ko">
<head>
  <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="description" content="{escape(description)}">
  {social_meta(title, description, canonical)}
  <link rel="canonical" href="{canonical}"><link rel="icon" href="../../favicon.svg" type="image/svg+xml"><title>{escape(title)}</title>
  {FONT_LINKS}<link rel="stylesheet" href="../../styles.css"><link rel="stylesheet" href="../../area.css">
  {structured}
</head>
<body>
  <header class="site-header" id="top"><a class="brand" href="../../" aria-label="대구 수학과외 홈"><span class="brand-mark" aria-hidden="true">Σ</span><span>대구 수학과외<small>STUDY PRO</small></span></a><button class="menu-button" type="button" aria-expanded="false" aria-controls="primary-nav" aria-label="메뉴 열기"><span></span><span></span><span></span></button><nav class="primary-nav" id="primary-nav" aria-label="주요 메뉴"><a href="#transition">학년별 수업</a><a href="#plan">수업 설계</a><a href="#nearby">인근 지역</a><a class="nav-cta" href="../../#contact">상담 신청</a></nav></header>
  <main>
    <section class="area-hero" aria-labelledby="area-title"><p class="breadcrumb"><a href="../../">대구 수학과외</a> / <a href="../">{escape(district_name)}</a> / {escape(locality)}</p><div class="area-hero-content"><p class="eyebrow light">{escape(district_name)} {escape(locality)} PERSONAL MATH</p><h1 id="area-title">대구 {escape(locality)} 수학과외,<br><em>이해를 성적으로 연결하는 수업</em></h1><p>{escape(locality)} 학생의 {place_phrase}과 학교 진도, 목표를 함께 살펴 개념 복습부터 내신·수능 대비까지 학생별 속도로 지도합니다.</p>{PHONE_BUTTON}</div></section>
    <section class="area-guide section" id="transition"><div class="area-guide-header reveal"><div><p class="eyebrow">GRADE TRANSITION</p><h2>다음 학년을 위한<br>빈틈 없는 준비</h2></div><p>{escape(locality)} 수학과외는 정답만 확인하지 않습니다. 풀이가 막힌 지점과 이전 개념의 빈틈을 먼저 찾고, 학교 수업과 다음 학년에서 필요한 내용을 순서대로 연결합니다.</p></div><div class="transition-grid">
      <article class="transition-card reveal"><small>MIDDLE SCHOOL</small><h3>예비중1 · 예비중2 · 예비중3</h3><p><strong>예비중1</strong>은 연산과 문자식의 기초를, <strong>예비중2</strong>는 방정식과 함수의 연결을 익힙니다. <strong>예비중3</strong>은 고등 수학으로 이어지는 대수와 도형 개념을 정리합니다.</p></article>
      <article class="transition-card reveal"><small>HIGH SCHOOL</small><h3>예비고1 · 예비고2 · 예비고3</h3><p><strong>예비고1</strong>은 공통수학의 개념과 학습량을 준비하고, <strong>예비고2</strong>는 내신과 선택 과목을 함께 설계합니다. <strong>예비고3</strong>은 기출과 취약 단원을 중심으로 수능 실전력을 높입니다.</p></article>
      <article class="transition-card reveal"><small>PERSONAL CARE</small><h3>{escape(locality)} 학생별 맞춤 관리</h3><p>같은 학년이라도 이해도와 목표는 다릅니다. 진단 결과와 학교 일정을 반영해 개념, 유형, 심화, 오답 복습의 비중을 조정합니다.</p></article>
    </div></section>
    {grades}
    <section class="local-plan section" id="plan"><div class="local-plan-inner"><div class="reveal"><p class="eyebrow light">LOCAL STUDY PLAN</p><h2>{escape(locality)} 학생을 위한<br>세밀한 학습 설계</h2></div><ol class="local-plan-list reveal"><li><span>01</span><div><strong>현재 실력 진단</strong><p>개념 이해도와 풀이 습관, 반복되는 실수의 원인을 확인합니다.</p></div></li><li><span>02</span><div><strong>학교 진도와 내신 연결</strong><p>시험 범위와 목표 점수에 맞춰 개념부터 서술형까지 준비합니다.</p></div></li><li><span>03</span><div><strong>복습과 오답 관리</strong><p>수업 후에도 혼자 설명하고 풀 수 있도록 주간 복습을 점검합니다.</p></div></li></ol></div></section>
    <section class="nearby section" id="nearby"><p class="eyebrow">{escape(district_name)} MATH AREA</p><h2>{escape(district_name)} 동·읍·면 수학과외</h2><div class="locality-links">{nearby}</div></section>
  </main>
  <footer><a class="brand" href="../../"><span class="brand-mark" aria-hidden="true">Σ</span><span>대구 수학과외<small>STUDY PRO</small></span></a><p>대구 {escape(district_name)} {escape(locality)} 초·중·고 1:1 맞춤 수학과외<br>상담 문의 <a href="tel:01029283614">010-2928-3614</a></p><p>© <span id="year"></span> STUDY PRO.</p></footer><a class="floating-contact" href="../../#contact" aria-label="상담 신청">상담<span aria-hidden="true">↗</span></a><script src="../../script.js?v=20261002"></script>
</body></html>
'''


def grade_url(district_slug: str | None, grade_slug: str) -> str:
    return f"{SITE_URL}/{district_slug}/{grade_slug}/" if district_slug else f"{SITE_URL}/{grade_slug}/"


def render_grade_page(district_slug: str | None, grade_slug: str) -> str:
    grade = GRADES[grade_slug]
    grade_name = grade["name"]
    if district_slug:
        district_name, localities = DISTRICTS[district_slug]
        short, place, root = district_name, f"대구 {district_name}", "../../"
    else:
        district_name, localities = None, []
        short, place, root = "대구", "대구", "../"
    canonical = grade_url(district_slug, grade_slug)
    title = f"{place} {grade_name} 수학과외 | {grade['title_tail']}"
    description = grade["description"].format(place=place)
    crumbs = [("대구 수학과외", f"{SITE_URL}/")]
    if district_slug:
        crumbs.append((f"{district_name} 수학과외", f"{SITE_URL}/{district_slug}/"))
    crumbs.append((f"{short} {grade_name} 수학과외", canonical))
    structured = "".join(json_ld(data) for data in (
        organization_ld(f"{place} {grade_name} 수학과외", canonical, f"대구광역시 {district_name}" if district_name else "대구광역시"),
        breadcrumb_ld(crumbs),
        faq_ld(grade["faqs"]),
    ))
    breadcrumb = f'<a href="{root}">대구 수학과외</a> / '
    if district_slug:
        breadcrumb += f'<a href="../">{escape(district_name)}</a> / '
    breadcrumb += f"{grade_name} 수학"

    cards = "".join(
        f'<article class="transition-card reveal"><small>{label}</small><h3>{escape(short)} {escape(heading)}</h3><p>{escape(text)}</p></article>'
        for label, heading, text in grade["cards"]
    )
    grid_class = "transition-grid grid-2" if len(grade["cards"]) == 4 else "transition-grid"
    stages = "".join(
        f'<li><span>{number:02d}</span><div><strong>{escape(short)} {escape(heading)}</strong><p>{escape(text)}</p></div></li>'
        for number, (heading, text) in enumerate(grade["stages"], 1)
    )
    faqs = "".join(
        f'<details{" open" if number == 0 else ""}><summary>{escape(question)}<span aria-hidden="true">+</span></summary><p>{escape(answer)}</p></details>'
        for number, (question, answer) in enumerate(grade["faqs"])
    )
    if district_slug:
        area_links = "".join(
            f'<a href="../locality-{number:02d}/">{escape(locality)} {grade_name} 수학 <span aria-hidden="true">↗</span></a>'
            for number, locality in enumerate(localities, 1)
        )
        area_section = (
            f'<section class="localities section" id="localities"><p class="eyebrow">{escape(district_name)} LOCAL AREA</p>'
            f'<h2>{escape(district_name)} 동네별 {grade_name} 수학과외</h2>'
            f'<p class="localities-intro">{REPRESENTATIVE_AREAS[district_slug]} 등 {escape(district_name)} 전 지역 {grade_name} 학생을 대상으로 수업합니다. 거주 지역을 선택해 동네별 안내를 확인하세요.</p>'
            f'<div class="locality-links">{area_links}</div></section>'
        )
        other_area_links = "".join(
            f'<a href="../../{slug}/{grade_slug}/">{escape(name)} {grade_name} 수학 <span aria-hidden="true">↗</span></a>'
            for slug, (name, _) in DISTRICTS.items() if slug != district_slug
        )
        other_grade_links = "".join(
            f'<a href="../{slug}/">{escape(district_name)} {other["name"]} 수학과외 <span aria-hidden="true">↗</span></a>'
            for slug, other in GRADES.items() if slug != grade_slug
        )
    else:
        area_links = "".join(
            f'<a href="../{slug}/{grade_slug}/">{escape(name)} {grade_name} 수학과외 <span aria-hidden="true">↗</span></a>'
            for slug, (name, _) in DISTRICTS.items()
        )
        area_section = (
            f'<section class="localities section" id="localities"><p class="eyebrow">DAEGU LOCAL AREA</p>'
            f'<h2>대구 지역별 {grade_name} 수학과외</h2>'
            f'<p class="localities-intro">대구 9개 구·군 {grade_name} 학생을 대상으로 수업합니다. 지역을 선택하면 가까운 동네의 {grade_name} 수학 수업 안내를 확인할 수 있습니다.</p>'
            f'<div class="locality-links">{area_links}</div></section>'
        )
        other_area_links = "".join(
            f'<a href="../{slug}/">{escape(name)} 수학과외 <span aria-hidden="true">↗</span></a>'
            for slug, (name, _) in DISTRICTS.items()
        )
        other_grade_links = "".join(
            f'<a href="../{slug}/">대구 {other["name"]} 수학과외 <span aria-hidden="true">↗</span></a>'
            for slug, other in GRADES.items() if slug != grade_slug
        )
    other_area_title = f"다른 지역 {grade_name} 수학과외" if district_slug else "대구 구·군별 수학과외"
    footer_area = f"대구 {district_name}" if district_name else "대구"
    return f'''<!doctype html>
<html lang="ko">
<head>
  <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="description" content="{escape(description)}">
  {social_meta(title, description, canonical)}
  <link rel="canonical" href="{canonical}"><link rel="icon" href="{root}favicon.svg" type="image/svg+xml"><title>{escape(title)}</title>
  {FONT_LINKS}<link rel="stylesheet" href="{root}styles.css"><link rel="stylesheet" href="{root}area.css">
  {structured}
</head>
<body>
  <header class="site-header" id="top"><a class="brand" href="{root}" aria-label="대구 수학과외 홈"><span class="brand-mark" aria-hidden="true">Σ</span><span>대구 수학과외<small>STUDY PRO</small></span></a><button class="menu-button" type="button" aria-expanded="false" aria-controls="primary-nav" aria-label="메뉴 열기"><span></span><span></span><span></span></button><nav class="primary-nav" id="primary-nav" aria-label="주요 메뉴"><a href="#lessons">수업 내용</a><a href="#stages">학년별 과정</a><a href="#localities">수업 지역</a><a class="nav-cta" href="{root}#contact">상담 신청</a></nav></header>
  <main>
    <section class="area-hero" aria-labelledby="area-title"><p class="breadcrumb">{breadcrumb}</p><div class="area-hero-content"><p class="eyebrow light">{escape(short)} {grade["eyebrow"]}</p><h1 id="area-title">{escape(place)} {grade_name} 수학과외,<br><em>{grade["tagline"]}</em></h1><p>{escape(grade["intro"].format(short=short))}</p>{PHONE_BUTTON}</div></section>
    <section class="area-guide section" id="lessons"><div class="area-guide-header reveal"><div><p class="eyebrow">{grade["eyebrow"]}</p><h2>{escape(short)} {grade["lesson_heading"]}</h2></div><p>{escape(grade["lesson_text"])}</p></div><div class="{grid_class}">{cards}</div></section>
    <section class="local-plan section" id="stages"><div class="local-plan-inner"><div class="reveal"><p class="eyebrow light">GRADE STAGES</p><h2>{escape(short)} {grade_name}<br>학년별 수학과외</h2></div><ol class="local-plan-list reveal">{stages}</ol></div></section>
    {area_section}
    <section class="area-faq section"><div class="area-faq-heading reveal"><p class="eyebrow">FREQUENTLY ASKED</p><h2>{escape(short)} {grade_name} 수학과외<br>자주 묻는 질문</h2><p>수업 시작 전에 궁금한 내용을 확인해 보세요.</p></div><div class="area-faq-list reveal">{faqs}</div></section>
    <section class="nearby section" id="nearby"><p class="eyebrow">MORE PROGRAM</p><h2>다른 학년 수학과외</h2><div class="nearby-links">{other_grade_links}</div><h2 class="nearby-subtitle">{other_area_title}</h2><div class="nearby-links">{other_area_links}</div></section>
    <section class="area-cta"><div class="area-cta-inner reveal"><div><p class="eyebrow light">START TOGETHER</p><h2>{escape(short)} {grade_name} 수학,<br>지금 상담해 보세요</h2><p>학생의 학년과 최근 성적, 어려워하는 단원을 알려주시면 필요한 수업 방향부터 안내해 드립니다.</p></div><div class="area-cta-actions"><a href="{root}#contact">무료 학습 상담 <span aria-hidden="true">↗</span></a><a href="tel:01029283614"><small>전화 상담</small><strong>010-2928-3614</strong></a></div></div></section>
  </main>
  <footer><a class="brand" href="{root}"><span class="brand-mark" aria-hidden="true">Σ</span><span>대구 수학과외<small>STUDY PRO</small></span></a><p>{escape(footer_area)} {grade_name} 1:1 맞춤 수학과외<br>상담 문의 <a href="tel:01029283614">010-2928-3614</a></p><p>© <span id="year"></span> STUDY PRO.</p></footer><a class="floating-contact" href="{root}#contact" aria-label="상담 신청">상담<span aria-hidden="true">↗</span></a><script src="{root}script.js?v=20261019"></script>
</body></html>
'''


def generate_grade_pages() -> list[str]:
    urls = []
    for district_slug in [None, *DISTRICTS]:
        for grade_slug in GRADES:
            base = ROOT / district_slug if district_slug else ROOT
            page_path = base / grade_slug / "index.html"
            page_path.parent.mkdir(exist_ok=True)
            page_path.write_text(render_grade_page(district_slug, grade_slug), encoding="utf-8", newline="\n")
            urls.append(grade_url(district_slug, grade_slug))
    return urls


def generate_pages() -> list[str]:
    urls = []
    for district_slug, (district_name, localities) in DISTRICTS.items():
        update_parent(district_slug, district_name, localities)
        district_path = ROOT / district_slug
        expected_directories = {f"locality-{index:02d}" for index in range(1, len(localities) + 1)}
        for old_path in district_path.glob("locality-*"):
            if old_path.is_dir() and old_path.name not in expected_directories:
                for child in old_path.iterdir():
                    child.unlink()
                old_path.rmdir()
        for index, locality in enumerate(localities, 1):
            page_path = district_path / f"locality-{index:02d}" / "index.html"
            page_path.parent.mkdir(exist_ok=True)
            page_path.write_text(
                render_page(district_slug, district_name, locality, index, localities),
                encoding="utf-8",
                newline="\n",
            )
            urls.append(f"{SITE_URL}/{district_slug}/locality-{index:02d}/")
    return urls


def update_sitemap(urls: list[str], grade_urls: list[str]) -> None:
    path = ROOT / "sitemap.xml"
    ET.register_namespace("", "http://www.sitemaps.org/schemas/sitemap/0.9")
    tree = ET.parse(path)
    root = tree.getroot()
    namespace = "{http://www.sitemaps.org/schemas/sitemap/0.9}"
    generated = set(grade_urls)
    for node in list(root):
        location = node.find(f"{namespace}loc")
        text = (location.text or "") if location is not None else ""
        if "/locality-" in text or text in generated:
            root.remove(node)
    last_modified = datetime.now(SEOUL_TIMEZONE).date().isoformat()
    for url_list, priority in ((grade_urls, "0.8"), (urls, "0.7")):
        for url in url_list:
            node = ET.SubElement(root, f"{namespace}url")
            ET.SubElement(node, f"{namespace}loc").text = url
            ET.SubElement(node, f"{namespace}lastmod").text = last_modified
            ET.SubElement(node, f"{namespace}changefreq").text = "monthly"
            ET.SubElement(node, f"{namespace}priority").text = priority
    ET.indent(tree, space="  ")
    tree.write(path, encoding="utf-8", xml_declaration=True)


def validate(urls: list[str], grade_urls: list[str]) -> None:
    if len(urls) != EXPECTED_PAGE_COUNT or len(set(urls)) != EXPECTED_PAGE_COUNT:
        raise ValueError(f"Expected {EXPECTED_PAGE_COUNT} unique pages, got {len(set(urls))}")
    if len(set(grade_urls)) != EXPECTED_GRADE_PAGE_COUNT:
        raise ValueError(f"Expected {EXPECTED_GRADE_PAGE_COUNT} grade pages, got {len(set(grade_urls))}")
    for url in grade_urls:
        page = ROOT / url.removeprefix(f"{SITE_URL}/") / "index.html"
        text = page.read_text(encoding="utf-8")
        if f'<link rel="canonical" href="{url}">' not in text or text.count("<title>") != 1:
            raise ValueError(f"Invalid head in {page}")
        for match in re.findall(r'<script type="application/ld\+json">(.*?)</script>', text):
            json.loads(match)
    for district_slug, (district_name, localities) in DISTRICTS.items():
        parent_text = (ROOT / district_slug / "index.html").read_text(encoding="utf-8")
        if parent_text.count("<title>") != 1 or parent_text.count('<link rel="canonical"') != 1:
            raise ValueError(f"Invalid head in {district_name} parent page")
        parent_links = re.findall(r'href="(locality-\d{2}/)"', parent_text)
        if len(parent_links) != len(localities) or len(parent_links) != len(set(parent_links)):
            raise ValueError(f"Invalid parent links for {district_name}")
        for index, locality in enumerate(localities, 1):
            page = ROOT / district_slug / f"locality-{index:02d}" / "index.html"
            text = page.read_text(encoding="utf-8")
            expected_url = f"{SITE_URL}/{district_slug}/locality-{index:02d}/"
            if f'<link rel="canonical" href="{expected_url}">' not in text:
                raise ValueError(f"Invalid canonical in {page}")
            if locality not in text or f'href="../">{district_name}</a>' not in text:
                raise ValueError(f"Invalid local content in {page}")
            if text.count(PHONE_BUTTON) != 1:
                raise ValueError(f"Invalid phone button in {page}")
    sitemap = ET.parse(ROOT / "sitemap.xml")
    namespace = "{http://www.sitemaps.org/schemas/sitemap/0.9}"
    sitemap_urls = [node.text for node in sitemap.findall(f".//{namespace}loc")]
    if sum(url in set(urls) for url in sitemap_urls) != EXPECTED_PAGE_COUNT:
        raise ValueError("Locality sitemap entries are missing or duplicated")
    if sum(url in set(grade_urls) for url in sitemap_urls) != EXPECTED_GRADE_PAGE_COUNT:
        raise ValueError("Grade sitemap entries are missing or duplicated")


def main() -> None:
    urls = generate_pages()
    grade_urls = generate_grade_pages()
    update_sitemap(urls, grade_urls)
    validate(urls, grade_urls)
    print(
        f"Generated and validated {len(urls)} locality pages and {len(grade_urls)} grade pages "
        f"across {len(DISTRICTS)} districts"
    )


if __name__ == "__main__":
    main()