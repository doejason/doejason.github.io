import json
import os
import re

# 1. Markdown 파일 표 rows 만들기 (2사분면)
POSTS_DIR = 'posts'
rows = []
for md in os.listdir(POSTS_DIR):
    if not md.endswith('.md'):
        continue
    md_path = os.path.join(POSTS_DIR, md)
    txt_name = os.path.splitext(md)[0] + '.txt'
    txt_path = os.path.join(POSTS_DIR, txt_name)
    # 날짜
    date_match = re.search(r'photo_(\d{8})', md)
    if date_match:
        raw_date = date_match.group(1)
        date_str = f"{raw_date[:4]}-{raw_date[4:6]}-{raw_date[6:]}"
    else:
        date_str = "(날짜없음)"
    origin_name = re.sub(r'^photo_\d{8}_Preview_page_\d+_of_', '', md)
    # 요약
    if os.path.exists(txt_path):
        with open(txt_path, encoding='utf-8') as f:
            summary = f.read().strip()
        lines = summary.split('\n', 1)
        if len(lines) == 2:
            keyword_line, body_line = lines[0], lines[1]
        else:
            keyword_line, body_line = lines[0], ""
        # 해시태그 파랑
        keyword_html = re.sub(r'(#[\w가-힣]+)', r'<span class="hashtag">\1</span>', keyword_line.strip())
        body_html = f'<div class="body-line">{body_line.strip()}</div>' if body_line.strip() else ""
        summary_html = f'<span class="summary-cell"><div class="hashtag-line">{keyword_html}</div>{body_html}</span>'
    else:
        summary_html = "(요약 없음)"
    md_link = f'<a href="{os.path.join(POSTS_DIR, md)}" title="{md}">{origin_name}</a>'
    rows.append(
        f"<tr>"
        f"<td class='summary'>{summary_html}</td>"
        f"<td class='origin'>{md_link}</td>"
        f"<td class='date'>{date_str}</td>"
        f"</tr>"
    )

# 2. 네이버 블로그 표 rows 만들기 (3사분면)
with open('blog_posts.json', encoding='utf-8') as jf:
    blog_posts = json.load(jf)

naver_rows = []
for post in blog_posts:
    # 날짜 예쁘게
    postdate = post.get('postdate', '')
    if len(postdate) == 8:
        date_str = f"{postdate[:4]}-{postdate[4:6]}-{postdate[6:]}"
    else:
        date_str = postdate
    title = post.get('title', '')
    link = post.get('link', '')
    blogger = post.get('bloggername', '')
    # 블로그 링크
    title_html = f'<a href="{link}" target="_blank">{title}</a>'
    naver_rows.append(
        f"<tr>"
        f"<td class='summary'>{title_html}</td>"
        f"<td class='origin'>{blogger}</td>"
        f"<td class='date'>{date_str}</td>"
        f"</tr>"
    )

naver_table = f"""
<div class="blog-title" style="font-size:24px; font-weight:600; color:#368748; margin-bottom:20px;">네이버 블로그</div>
<table class="table-fixed">
  <thead>
    <tr>
      <th class="summary">제목</th>
      <th class="origin">블로거</th>
      <th class="date">날짜</th>
    </tr>
  </thead>
  <tbody>
    {''.join(naver_rows)}
  </tbody>
</table>
"""

# 3. 전체 HTML 출력
html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Markdown List</title>
<style>
body {{
  margin: 0;
  padding: 0;
  background: transparent;
  font-family: 'Pretendard', 'Apple SD Gothic Neo', Arial, sans-serif;
  font-size: 13px;
}}
.row-wrapper {{
  position: fixed;
  left: 0;
  top: 0;
  width: 100vw;
  height: 50vh;
  display: flex;
  z-index: 10;
  background: transparent;
}}
.sector-label-box {{
  width: 50vw;
  height: 100%;
  background: transparent;
  display: flex;
  align-items: flex-start;
  justify-content: flex-start;
  font-size: 26px;
  font-weight: 600;
  color: #2b3687;
  padding: 42px 0 0 46px;
  user-select: none;
  pointer-events: none;
}}
.main-table-wrapper {{
  width: 50vw;
  height: 100%;
  background: transparent;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}}
h1 {{
  margin: 16px 0 8px 0;
  font-size: 1.05em;
  padding-left: 24px;
  background: transparent;
}}
.table-fixed {{
  table-layout: fixed;
  width: 100%;
  font-size: 13px;
  border-collapse: collapse;
  background: transparent;
  border: 1.5px solid #d6d7db;
}}
th, td {{
  font-size: 13px;
  padding: 6px 10px;
  background: transparent;
  border: 1px solid #b6b7be;
}}
th.summary, td.summary {{
  width: 58%;
  min-width: 160px;
  max-width: 600px;
  vertical-align: top;
}}
th.origin, td.origin {{
  width: 20%;
  min-width: 55px;
  max-width: 100px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}}
th.date, td.date {{
  width: 22%;
  min-width: 90px;
  max-width: 130px;
}}
td.origin a {{
  display: inline-block;
  vertical-align: middle;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  font-size: 13px;
  background: transparent;
}}
.summary-cell {{
  display: block;
  white-space: normal;
  line-height: 1.4;
  background: transparent;
}}
.hashtag {{
  color: #1e6aff;
  font-weight: bold;
  font-size: 13px;
  background: transparent;
}}
.hashtag-line {{
  margin-bottom: 3px;
  font-size: 13px;
  background: transparent;
}}
.body-line {{
  color: #222;
  font-size: 13px;
  margin-bottom: 2px;
  background: transparent;
}}
.table-scroll-body {{
  overflow-y: auto;
  height: calc(50vh - 54px);
  background: transparent;
}}
/* 3사분면 - 네이버 블로그 (왼쪽 아래) */
.blog-label-box {{
  position: fixed;
  left: 0;
  bottom: 0;
  width: 50vw;
  height: 50vh;
  background: transparent;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  justify-content: flex-start;
  padding: 42px 0 0 46px;
  user-select: none;
  pointer-events: auto;
  z-index: 10;
  overflow-y: auto;
}}
.blog-title {{
  font-size: 22px;
  color: #368748;
  font-weight: bold;
  margin-bottom: 5px;
}}
.table-fixed a {{
  color: #2571cb;
  text-decoration: underline dotted;
}}
</style>
</head>
<body>
<div class="row-wrapper">
  <div class="sector-label-box">섹터</div>
  <div class="main-table-wrapper">
    <h1>Markdown Files</h1>
    <div class="table-scroll-body">
      <table class="table-fixed">
        <thead>
        <tr>
            <th class="summary">요약</th>
            <th class="origin">원본(markdown)</th>
            <th class="date">날짜</th>
        </tr>
        </thead>
        <tbody>
        {''.join(rows)}
        </tbody>
      </table>
    </div>
  </div>
</div>
<div class="blog-label-box">
  {naver_table}
</div>
</body>
</html>
"""

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
