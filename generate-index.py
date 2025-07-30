# import os
# import re

# POSTS_DIR = 'posts'
# INDEX_FILE = 'index.html'

# def color_hashtags(text):
#     return re.sub(r'(#[\w가-힣]+)', r'<span class="hashtag">\1</span>', text)

# data = []
# for md in os.listdir(POSTS_DIR):
#     if not md.endswith('.md'):
#         continue
#     md_path = os.path.join(POSTS_DIR, md)
#     txt_name = os.path.splitext(md)[0] + '.txt'
#     txt_path = os.path.join(POSTS_DIR, txt_name)

#     # 날짜 추출
#     date_match = re.search(r'photo_(\d{8})', md)
#     if date_match:
#         raw_date = date_match.group(1)
#         date_sort_key = raw_date
#         date_str = f"{raw_date[:4]}-{raw_date[4:6]}-{raw_date[6:8]}"
#     else:
#         date_sort_key = "00000000"
#         date_str = "(날짜없음)"

#     # 원본파일명에서 'photo_YYYYMMDD_Preview_page_N_of_' 앞부분 제거
#     origin_name = re.sub(r'^photo_\d{8}_Preview_page_\d+_of_', '', md)

#     # 요약(txt) 파일 분리 처리
#     if os.path.exists(txt_path):
#         with open(txt_path, encoding='utf-8') as f:
#             summary = f.read().strip()
#         lines = summary.split('\n', 1)
#         if len(lines) == 2:
#             keyword_line, body_line = lines[0], lines[1]
#         else:
#             keyword_line, body_line = lines[0], ""
#         keyword_html = f'<div class="hashtag-line">{color_hashtags(keyword_line.strip())}</div>'
#         body_html = f'<div class="body-line">{body_line.strip()}</div>' if body_line.strip() else ""
#         summary_html = f'<span class="summary-cell">{keyword_html}{body_html}</span>'
#     else:
#         summary_html = "(요약 없음)"

#     md_link = f'<a href="{os.path.join(POSTS_DIR, md)}" title="{md}">{origin_name}</a>'

#     data.append((date_sort_key, summary_html, md_link, date_str))

# # 날짜 내림차순
# data_sorted = sorted(data, key=lambda x: x[0], reverse=True)

# rows = [
#     f"<tr>"
#     f"<td class='summary'>{summary_html}</td>"
#     f"<td class='origin'>{md_link}</td>"
#     f"<td class='date'>{date_str}</td>"
#     f"</tr>"
#     for (_, summary_html, md_link, date_str) in data_sorted
# ]

# html = f"""<!DOCTYPE html>
# <html lang="en">
# <head>
# <meta charset="utf-8">
# <title>Markdown List</title>
# <style>
# .hashtag {{
#   color: #1e6aff;
#   font-weight: bold;
# }}
# .hashtag-line {{
#   margin-bottom: 4px;
# }}
# .body-line {{
#   color: #222;
#   margin-bottom: 2px;
#   font-size: 15px;
# }}
# .table-fixed {{
#   table-layout: fixed;
#   width: 100%;
# }}
# th.summary, td.summary {{
#   width: 60%;
#   min-width: 250px;
#   max-width: 700px;
#   vertical-align: top;
# }}
# th.origin, td.origin {{
#   width: 16%;
#   min-width: 55px;
#   max-width: 120px;
#   white-space: nowrap;
#   overflow: hidden;
#   text-overflow: ellipsis;
# }}
# th.date, td.date {{
#   width: 24%;
#   min-width: 90px;
#   max-width: 150px;
# }}
# td.origin a {{
#   display: inline-block;
#   vertical-align: middle;
#   white-space: nowrap;
#   overflow: hidden;
#   text-overflow: ellipsis;
# }}
# .summary-cell {{
#   display: block;
#   white-space: normal;
#   line-height: 1.6;
# }}
# </style>
# </head>
# <body>
# <h1>Markdown Files</h1>
# <table border="1" cellspacing="0" cellpadding="4" class="table-fixed">
# <thead>
# <tr>
#     <th class="summary">요약</th>
#     <th class="origin">원본(markdown)</th>
#     <th class="date">날짜</th>
# </tr>
# </thead>
# <tbody>
# {''.join(rows)}
# </tbody>
# </table>
# </body>
# </html>
# """

# with open(INDEX_FILE, 'w', encoding='utf-8') as f:
#     f.write(html)

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
  font-size: 13px;  /* 전체 글씨 크기 축소 */
}}
.main-table-wrapper {{
  position: fixed;
  right: 0;
  top: 0;
  width: 50vw;
  height: 50vh;
  background: #fff;
  box-shadow: 0 6px 24px rgba(0,0,0,0.08);
  border-radius: 20px 0 0 20px;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  border: 1.5px solid #e0e0e0;
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
/* 표 내 세로 스크롤 (헤더 고정 아님, 전체 스크롤) */
.table-scroll-body {{
  overflow-y: auto;
  height: calc(50vh - 54px); /* 상단 h1/padding 고려해서 약간 뺌 */
}}
</style>
</head>
<body>
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
</body>
</html>
"""

with open(INDEX_FILE, 'w', encoding='utf-8') as f:
    f.write(html)
