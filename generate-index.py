import os
import re

POSTS_DIR = 'posts'
INDEX_FILE = 'index.html'

def color_hashtags(text):
    # #키워드만 파란색
    return re.sub(r'(#[\w가-힣]+)', r'<span class="hashtag">\1</span>', text)

data = []
for md in os.listdir(POSTS_DIR):
    if not md.endswith('.md'):
        continue
    md_path = os.path.join(POSTS_DIR, md)
    txt_name = os.path.splitext(md)[0] + '.txt'
    txt_path = os.path.join(POSTS_DIR, txt_name)

    # 날짜 추출
    date_match = re.search(r'photo_(\d{8})', md)
    if date_match:
        raw_date = date_match.group(1)
        date_sort_key = raw_date
        date_str = f"{raw_date[:4]}-{raw_date[4:6]}-{raw_date[6:8]}"
    else:
        date_sort_key = "00000000"
        date_str = "(날짜없음)"

    # 원본파일명에서 'photo_YYYYMMDD_Preview_page_N_of_' 앞부분 제거
    origin_name = re.sub(r'^photo_\d{8}_Preview_page_\d+_of_', '', md)

    # 요약(txt) 파일 분리 처리
    if os.path.exists(txt_path):
        with open(txt_path, encoding='utf-8') as f:
            summary = f.read().strip()
        lines = summary.split('\n', 1)
        if len(lines) == 2:
            keyword_line, _ = lines[0], lines[1]
        else:
            keyword_line = lines[0]
        keyword_html = f'<div class="hashtag-line">{color_hashtags(keyword_line.strip())}</div>'
        # 표에는 키워드 한 줄만!
        summary_html = f'<span class="summary-cell">{keyword_html}</span>'
    else:
        summary_html = "(요약 없음)"

    md_link = f'<a href="{os.path.join(POSTS_DIR, md)}" title="{md}">{origin_name}</a>'

    data.append((date_sort_key, summary_html, md_link, date_str))

# 날짜 내림차순
data_sorted = sorted(data, key=lambda x: x[0], reverse=True)

rows = [
    f"<tr>"
    f"<td class='summary'>{summary_html}</td>"
    f"<td class='origin'>{md_link}</td>"
    f"<td class='date'>{date_str}</td>"
    f"</tr>"
    for (_, summary_html, md_link, date_str) in data_sorted
]

html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Markdown List</title>
<style>
.hashtag {{
  color: #1e6aff;
  font-weight: bold;
}}
.hashtag-line {{
  margin-bottom: 2px;
}}
.table-fixed {{
  table-layout: fixed;
  width: 100%;
}}
th.summary, td.summary {{
  width: 60%;
  min-width: 250px;
  max-width: 700px;
}}
th.origin, td.origin {{
  width: 16%;
  min-width: 55px;
  max-width: 120px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}}
th.date, td.date {{
  width: 24%;
  min-width: 90px;
  max-width: 150px;
}}
td.origin a {{
  display: inline-block;
  vertical-align: middle;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}}
</style>
</head>
<body>
<h1>Markdown Files</h1>
<table border="1" cellspacing="0" cellpadding="4" class="table-fixed">
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
</body>
</html>
"""

with open(INDEX_FILE, 'w', encoding='utf-8') as f:
    f.write(html)
