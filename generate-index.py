import os
import re

POSTS_DIR = 'posts'
INDEX_FILE = 'index.html'

def color_hashtags(text):
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

    origin_name = re.sub(r'^photo_\d{8}_Preview_page_\d+_of_', '', md)

    # 요약(txt) 파일 분리 처리
    if os.path.exists(txt_path):
        with open(txt_path, encoding='utf-8') as f:
            summary = f.read().strip()
        lines = summary.split('\n', 1)
        if len(lines) == 2:
            keyword_line, body_line = lines[0], lines[1]
        else:
            keyword_line, body_line = lines[0], ""
        keyword_html = f'<div class="hashtag-line">{color_hashtags(keyword_line.strip())}</div>'
        body_html = f'<div class="body-line">{body_line.strip()}</div>' if body_line.strip() else ""
        summary_html = f'<span class="summary-cell">{keyword_html}{body_html}</span>'
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
body {{
  margin: 0;
  padding: 0;
  background: #fcfcfc;
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
}}

/* 섹터 박스 - 왼쪽 */
.sector-label-box {{
  width: 50vw;
  height: 100%;
  background: #fff;
  /* border-radius: 0 0 0 38px; */
  border-radius: 0;
  box-shadow: 0 2px 14px rgba(0,0,0,0.04);
  display: flex;
  align-items: flex-start;
  justify-content: flex-start;
  font-size: 26px;
  font-weight: 600;
  color: #2b3687;
  padding: 44px 0 0 46px;
  border-right: 1.5px solid #e0e0e0;
}}

/* 표 wrapper - 오른쪽 */
.main-table-wrapper {{
  width: 50vw;
  height: 100%;
  background: #fff;
  box-shadow: 0 6px 24px rgba(0,0,0,0.08);
  /* border-radius: 0 0 20px 0; */
  border-radius: 0;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  border-left: none;
}}
h1 {{
  margin: 16px 0 8px 0;
  font-size: 1.05em;
  padding-left: 24px;
}}
.table-fixed {{
  table-layout: fixed;
  width: 100%;
  font-size: 13px;
  border-collapse: collapse;
}}
th, td {{
  font-size: 13px;
  padding: 6px 10px;
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
}}
.summary-cell {{
  display: block;
  white-space: normal;
  line-height: 1.4;
}}
.hashtag {{
  color: #1e6aff;
  font-weight: bold;
  font-size: 13px;
}}
.hashtag-line {{
  margin-bottom: 3px;
  font-size: 13px;
}}
.body-line {{
  color: #222;
  font-size: 13px;
  margin-bottom: 2px;
}}
.table-scroll-body {{
  overflow-y: auto;
  height: calc(50vh - 54px);
}}
</style>
</head>
<body>
<div class="row-wrapper">
  <div class="sector-label-box">섹터</div>
  <div class="main-table-wrapper">
    <h1>Markdown Files</h1>
    <div class="table-scroll-body">
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
    </div>
  </div>
</div>
</body>
</html>
"""


with open(INDEX_FILE, 'w', encoding='utf-8') as f:
    f.write(html)
