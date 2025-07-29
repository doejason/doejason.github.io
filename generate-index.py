# import os
# import re

# POSTS_DIR = 'posts'
# INDEX_FILE = 'index.html'

# # 날짜, md파일명, 나머지 정보 미리 추출해서 리스트에 담기
# data = []
# for md in os.listdir(POSTS_DIR):
#     if not md.endswith('.md'):
#         continue
#     md_path = os.path.join(POSTS_DIR, md)
#     txt_name = os.path.splitext(md)[0] + '.txt'
#     txt_path = os.path.join(POSTS_DIR, txt_name)

#     # 날짜 추출 (photo_YYYYMMDD_...)
#     date_match = re.search(r'photo_(\d{8})', md)
#     if date_match:
#         raw_date = date_match.group(1)
#         date_sort_key = raw_date  # for sorting
#         date_str = f"{raw_date[:4]}-{raw_date[4:6]}-{raw_date[6:8]}"
#     else:
#         date_sort_key = "00000000"
#         date_str = "(날짜없음)"

#     # 원본파일명에서 'photo_YYYYMMDD_Preview_page_N_of_' 앞부분 제거
#     origin_name = re.sub(r'^photo_\d{8}_Preview_page_\d+_of_', '', md)

#     # 요약(txt) 내용 읽기
#     if os.path.exists(txt_path):
#         with open(txt_path, encoding='utf-8') as f:
#             summary = f.read().strip().replace('\n', ' ')
#         short_summary = summary[:60] + ('...' if len(summary) > 60 else '')
#         summary_html = f'<span class="summary-cell" data-summary="{summary}">{short_summary}</span>'
#     else:
#         summary_html = "(요약 없음)"

#     md_link = f'<a href="{os.path.join(POSTS_DIR, md)}" title="{md}">{origin_name}</a>'

#     data.append((date_sort_key, summary_html, md_link, date_str))

# # 날짜 내림차순으로 정렬 (최신이 위)
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
# .tooltip-box {{
#   display: none;
#   position: absolute;
#   z-index: 9999;
#   background: #fff;
#   border: 1px solid #aaa;
#   padding: 14px 18px;
#   border-radius: 9px;
#   color: #222;
#   font-size: 15px;
#   box-shadow: 0 4px 16px rgba(0,0,0,0.12);
#   max-width: 420px;
#   min-width: 120px;
#   word-break: break-all;
#   user-select: text;
# }}
# .summary-cell {{
#   cursor: pointer;
# }}
# .table-fixed {{
#   table-layout: fixed;
#   width: 100%;
# }}
# th.summary, td.summary {{
#   width: 60%;
#   min-width: 250px;
#   max-width: 700px;
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

# <div id="tooltip" class="tooltip-box"></div>
# <script>
# const tooltip = document.getElementById('tooltip');
# let currentTarget = null;

# document.querySelectorAll('.summary-cell').forEach(cell => {{
#   cell.addEventListener('mouseover', function(e) {{
#     currentTarget = cell;
#     tooltip.textContent = cell.getAttribute('data-summary');
#     tooltip.style.display = 'block';
#     const rect = cell.getBoundingClientRect();
#     tooltip.style.left = (rect.left + window.scrollX) + 'px';
#     tooltip.style.top = (rect.bottom + window.scrollY + 8) + 'px';
#   }});
# }});

# tooltip.addEventListener('mouseover', function() {{
#   // do nothing
# }});

# document.addEventListener('mousemove', function(e) {{
#   let overSummary = false;
#   let overTooltip = false;
#   let el = e.target;
#   while (el) {{
#     if (el.classList && el.classList.contains('summary-cell')) overSummary = true;
#     if (el.id === 'tooltip') overTooltip = true;
#     el = el.parentElement;
#   }}
#   if (!(overSummary || overTooltip)) {{
#     tooltip.style.display = 'none';
#     currentTarget = null;
#   }}
# }});
# </script>
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

    # 원본파일명에서 'photo_YYYYMMDD_Preview_page_N_of_' 앞부분 제거
    origin_name = re.sub(r'^photo_\d{8}_Preview_page_\d+_of_', '', md)

    # 요약(txt) 내용 읽기
    if os.path.exists(txt_path):
        with open(txt_path, encoding='utf-8') as f:
            summary = f.read().strip().replace('\n', ' ')
        # 해시태그 파란색 처리
        summary_colored = color_hashtags(summary)
        # 짧은 버전도 해시태그 포함
        short_summary = summary_colored[:60] + ('...' if len(summary_colored) > 60 else '')
        # data-summary에도 색 입힘(툴팁도 html 지원)
        summary_html = f'<span class="summary-cell" data-summary="{summary_colored}">{short_summary}</span>'
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
}}
.hashtag {{
  color: #1e6aff;
  font-weight: bold;
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

<div id="tooltip" class="tooltip-box"></div>
<script>
const tooltip = document.getElementById('tooltip');
let currentTarget = null;

document.querySelectorAll('.summary-cell').forEach(cell => {{
  cell.addEventListener('mouseover', function(e) {{
    currentTarget = cell;
    // innerHTML로 변경해서 html 태그 포함 표시 (파란색 해시태그 지원)
    tooltip.innerHTML = cell.getAttribute('data-summary');
    tooltip.style.display = 'block';
    const rect = cell.getBoundingClientRect();
    tooltip.style.left = (rect.left + window.scrollX) + 'px';
    tooltip.style.top = (rect.bottom + window.scrollY + 8) + 'px';
  }});
}});

tooltip.addEventListener('mouseover', function() {{
  // do nothing
}});

document.addEventListener('mousemove', function(e) {{
  let overSummary = false;
  let overTooltip = false;
  let el = e.target;
  while (el) {{
    if (el.classList && el.classList.contains('summary-cell')) overSummary = true;
    if (el.id === 'tooltip') overTooltip = true;
    el = el.parentElement;
  }}
  if (!(overSummary || overTooltip)) {{
    tooltip.style.display = 'none';
    currentTarget = null;
  }}
}});
</script>
</body>
</html>
"""

with open(INDEX_FILE, 'w', encoding='utf-8') as f:
    f.write(html)
