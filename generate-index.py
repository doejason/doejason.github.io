import os
import re

POSTS_DIR = 'posts'
INDEX_FILE = 'index.html'

md_files = sorted([f for f in os.listdir(POSTS_DIR) if f.endswith('.md')])

rows = []
for md in md_files:
    md_path = os.path.join(POSTS_DIR, md)
    txt_name = os.path.splitext(md)[0] + '.txt'
    txt_path = os.path.join(POSTS_DIR, txt_name)

    # 날짜 추출 (photo_YYYYMMDD_...)
    date_match = re.search(r'photo_(\d{8})', md)
    if date_match:
        raw_date = date_match.group(1)
        # YYYYMMDD → YYYY-MM-DD
        date_str = f"{raw_date[:4]}-{raw_date[4:6]}-{raw_date[6:8]}"
    else:
        date_str = "(날짜없음)"

    # 요약(txt) 내용 읽기
    if os.path.exists(txt_path):
        with open(txt_path, encoding='utf-8') as f:
            summary = f.read().strip().replace('\n', ' ')
        short_summary = summary[:40] + ('...' if len(summary) > 40 else '')
        summary_html = f'<span class="summary-cell" data-summary="{summary}">{short_summary}</span>'
    else:
        summary_html = "(요약 없음)"

    md_link = f'<a href="{md_path}">{md}</a>'
    rows.append(f"<tr><td>{summary_html}</td><td>{md_link}</td><td>{date_str}</td></tr>")

html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Markdown List</title>
<style>
.tooltip-box {{
  display: none;
  position: absolute;
  z-index: 9999;
  background: #fff;
  border: 1px solid #aaa;
  padding: 14px 18px;
  border-radius: 9px;
  color: #222;
  font-size: 15px;
  box-shadow: 0 4px 16px rgba(0,0,0,0.12);
  max-width: 420px;
  min-width: 120px;
  word-break: break-all;
  user-select: text;
}}
.summary-cell {{
  cursor: pointer;
  text-decoration: underline dotted;
}}
/* 표 전체 */
.table-fixed {{
  table-layout: fixed;
  width: 100%;
}}
/* 요약 컬럼 넓게, 원본 좁게, 날짜 중간 */
th.summary, td.summary {{
  width: 60%;
  min-width: 250px;
  max-width: 700px;
}}
th.origin, td.origin {{
  width: 25%;
  min-width: 80px;
  max-width: 230px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}}
th.date, td.date {{
  width: 15%;
  min-width: 90px;
  max-width: 150px;
}}
/* 원본 컬럼 a 태그도 잘리게 */
td.origin a {{
  display: inline-block;
  max-width: 200px;
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

<div id="tooltip" class="tooltip-box"></div>
<script>
// ... (툴팁 스크립트 동일)
</script>
</body>
</html>
"""


with open(INDEX_FILE, 'w', encoding='utf-8') as f:
    f.write(html)
