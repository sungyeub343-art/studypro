from datetime import date
from html import escape
from pathlib import Path
import re
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
SITE_URL = "https://studypro.kr"

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

EXPECTED_PAGE_COUNT = 150
GENERATED_START = "<!-- LOCALITY-LINKS:START -->"
GENERATED_END = "<!-- LOCALITY-LINKS:END -->"


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
    return (
        f'{GENERATED_START}\n'
        f'    <section class="localities section" id="localities"><p class="eyebrow">{escape(district_name)} LOCAL AREA</p>'
        f'<h2>{escape(district_name)} 동·읍·면 수학과외</h2><p class="localities-intro">거주 지역을 선택하면 가까운 곳에서 진행하는 1:1 맞춤 수업을 확인할 수 있습니다.</p>'
        f'<div class="locality-links">{links}</div></section>\n'
        f'    {GENERATED_END}\n'
    )


def update_parent(district_slug: str, district_name: str, localities: list[str]) -> None:
    path = ROOT / district_slug / "index.html"
    text = path.read_text(encoding="utf-8")
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
    title = f"대구 {district_name} {locality} 수학과외 | 초중고 1:1 맞춤 수업"
    description = (
        f"대구 {district_name} {locality} 수학과외 - 초등·중등·고등 학생의 현재 실력을 진단하고 "
        "예비중1·예비중2·예비중3·예비고1·예비고2·예비고3 내신과 수능을 1:1로 준비합니다."
    )
    place_phrase = {"동": "생활권", "읍": "통학 환경", "면": "지역과 통학 일정"}[kind]
    nearby = locality_links(localities, index)
    return f'''<!doctype html>
<html lang="ko">
<head>
  <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="description" content="{escape(description)}">
  <meta name="theme-color" content="#173b35"><meta property="og:type" content="website"><meta property="og:locale" content="ko_KR"><meta property="og:title" content="{escape(title)}"><meta property="og:description" content="{escape(locality)} 학생을 위한 초중고 1:1 맞춤 수학과외"><meta property="og:url" content="{canonical}">
  <link rel="canonical" href="{canonical}"><link rel="icon" href="../../favicon.svg" type="image/svg+xml"><title>{escape(title)}</title>
  <link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Gowun+Batang:wght@700&family=Noto+Sans+KR:wght@400;500;600;700;800&display=swap" rel="stylesheet"><link rel="stylesheet" href="../../styles.css"><link rel="stylesheet" href="../../area.css">
  <script type="application/ld+json">{{"@context":"https://schema.org","@type":"EducationalOrganization","name":"대구 {escape(district_name)} {escape(locality)} 수학과외","url":"{canonical}","telephone":"+82-10-2928-3614","areaServed":{{"@type":"Place","name":"대구광역시 {escape(district_name)} {escape(locality)}"}}}}</script>
</head>
<body>
  <header class="site-header" id="top"><a class="brand" href="../../" aria-label="대구 수학과외 홈"><span class="brand-mark" aria-hidden="true">Σ</span><span>대구 수학과외<small>STUDY PRO</small></span></a><button class="menu-button" type="button" aria-expanded="false" aria-controls="primary-nav" aria-label="메뉴 열기"><span></span><span></span><span></span></button><nav class="primary-nav" id="primary-nav" aria-label="주요 메뉴"><a href="#transition">학년별 수업</a><a href="#plan">수업 설계</a><a href="#nearby">인근 지역</a><a class="nav-cta" href="../../#contact">상담 신청</a></nav></header>
  <main>
    <section class="area-hero" aria-labelledby="area-title"><p class="breadcrumb"><a href="../../">대구 수학과외</a> / <a href="../">{escape(district_name)}</a> / {escape(locality)}</p><div class="area-hero-content"><p class="eyebrow light">{escape(district_name)} {escape(locality)} PERSONAL MATH</p><h1 id="area-title">대구 {escape(locality)} 수학과외,<br><em>이해를 성적으로 연결하는 수업</em></h1><p>{escape(locality)} 학생의 {place_phrase}과 학교 진도, 목표를 함께 살펴 개념 복습부터 내신·수능 대비까지 학생별 속도로 지도합니다.</p></div></section>
    <section class="area-guide section" id="transition"><div class="area-guide-header reveal"><div><p class="eyebrow">GRADE TRANSITION</p><h2>다음 학년을 위한<br>빈틈 없는 준비</h2></div><p>{escape(locality)} 수학과외는 정답만 확인하지 않습니다. 풀이가 막힌 지점과 이전 개념의 빈틈을 먼저 찾고, 학교 수업과 다음 학년에서 필요한 내용을 순서대로 연결합니다.</p></div><div class="transition-grid">
      <article class="transition-card reveal"><small>MIDDLE SCHOOL</small><h3>예비중1 · 예비중2 · 예비중3</h3><p><strong>예비중1</strong>은 연산과 문자식의 기초를, <strong>예비중2</strong>는 방정식과 함수의 연결을 익힙니다. <strong>예비중3</strong>은 고등 수학으로 이어지는 대수와 도형 개념을 정리합니다.</p></article>
      <article class="transition-card reveal"><small>HIGH SCHOOL</small><h3>예비고1 · 예비고2 · 예비고3</h3><p><strong>예비고1</strong>은 공통수학의 개념과 학습량을 준비하고, <strong>예비고2</strong>는 내신과 선택 과목을 함께 설계합니다. <strong>예비고3</strong>은 기출과 취약 단원을 중심으로 수능 실전력을 높입니다.</p></article>
      <article class="transition-card reveal"><small>PERSONAL CARE</small><h3>{escape(locality)} 학생별 맞춤 관리</h3><p>같은 학년이라도 이해도와 목표는 다릅니다. 진단 결과와 학교 일정을 반영해 개념, 유형, 심화, 오답 복습의 비중을 조정합니다.</p></article>
    </div></section>
    <section class="local-plan section" id="plan"><div class="local-plan-inner"><div class="reveal"><p class="eyebrow light">LOCAL STUDY PLAN</p><h2>{escape(locality)} 학생을 위한<br>세밀한 학습 설계</h2></div><ol class="local-plan-list reveal"><li><span>01</span><div><strong>현재 실력 진단</strong><p>개념 이해도와 풀이 습관, 반복되는 실수의 원인을 확인합니다.</p></div></li><li><span>02</span><div><strong>학교 진도와 내신 연결</strong><p>시험 범위와 목표 점수에 맞춰 개념부터 서술형까지 준비합니다.</p></div></li><li><span>03</span><div><strong>복습과 오답 관리</strong><p>수업 후에도 혼자 설명하고 풀 수 있도록 주간 복습을 점검합니다.</p></div></li></ol></div></section>
    <section class="nearby section" id="nearby"><p class="eyebrow">{escape(district_name)} MATH AREA</p><h2>{escape(district_name)} 동·읍·면 수학과외</h2><div class="locality-links">{nearby}</div></section>
  </main>
  <footer><a class="brand" href="../../"><span class="brand-mark" aria-hidden="true">Σ</span><span>대구 수학과외<small>STUDY PRO</small></span></a><p>대구 {escape(district_name)} {escape(locality)} 초·중·고 1:1 맞춤 수학과외<br>상담 문의 <a href="tel:01029283614">010-2928-3614</a></p><p>© <span id="year"></span> STUDY PRO.</p></footer><a class="floating-contact" href="../../#contact" aria-label="상담 신청">상담<span aria-hidden="true">↗</span></a><script src="../../script.js?v=20261002"></script>
</body></html>
'''


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


def update_sitemap(urls: list[str]) -> None:
    path = ROOT / "sitemap.xml"
    ET.register_namespace("", "http://www.sitemaps.org/schemas/sitemap/0.9")
    tree = ET.parse(path)
    root = tree.getroot()
    namespace = "{http://www.sitemaps.org/schemas/sitemap/0.9}"
    for node in list(root):
        location = node.find(f"{namespace}loc")
        if location is not None and "/locality-" in (location.text or ""):
            root.remove(node)
    last_modified = date.today().isoformat()
    for url in urls:
        node = ET.SubElement(root, f"{namespace}url")
        ET.SubElement(node, f"{namespace}loc").text = url
        ET.SubElement(node, f"{namespace}lastmod").text = last_modified
        ET.SubElement(node, f"{namespace}changefreq").text = "monthly"
        ET.SubElement(node, f"{namespace}priority").text = "0.7"
    ET.indent(tree, space="  ")
    tree.write(path, encoding="utf-8", xml_declaration=True)


def validate(urls: list[str]) -> None:
    if len(urls) != EXPECTED_PAGE_COUNT or len(set(urls)) != EXPECTED_PAGE_COUNT:
        raise ValueError(f"Expected {EXPECTED_PAGE_COUNT} unique pages, got {len(set(urls))}")
    for district_slug, (district_name, localities) in DISTRICTS.items():
        parent_text = (ROOT / district_slug / "index.html").read_text(encoding="utf-8")
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
    sitemap = ET.parse(ROOT / "sitemap.xml")
    namespace = "{http://www.sitemaps.org/schemas/sitemap/0.9}"
    sitemap_urls = [node.text for node in sitemap.findall(f".//{namespace}loc")]
    if sum(url in set(urls) for url in sitemap_urls) != EXPECTED_PAGE_COUNT:
        raise ValueError("Locality sitemap entries are missing or duplicated")


def main() -> None:
    urls = generate_pages()
    update_sitemap(urls)
    validate(urls)
    print(f"Generated and validated {len(urls)} locality pages across {len(DISTRICTS)} districts")


if __name__ == "__main__":
    main()