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

tbody_html = ''.join([
    f"<tr>"
    f"<td class='summary'>{summary_html}</td>"
    f"<td class='origin'>{md_link}</td>"
    f"<td class='date'>{date_str}</td>"
    f"</tr>"
    for (_, summary_html, md_link, date_str) in data_sorted
])

html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<title>AI 마크다운 요약 테이블</title>
<style>
body {{
  margin: 0;
  padding: 0;
  background: #f9fafd;
  font-family: 'Pretendard', 'Apple SD Gothic Neo', Arial, sans-serif;
  font-size: 14px;
  color: #212326;
}}
h1 {{
  font-size: 1.13em;
  margin: 22px 0 12px 18px;
  color: #254;
  letter-spacing: 0.01em;
}}
.hashtag {{
  color: #1976d2;
  font-weight: bold;
  font-size: 13px;
}}
.hashtag-line {{
  margin-bottom: 2.5px;
  font-size: 13px;
}}
.body-line {{
  color: #222;
  margin-bottom: 1px;
  font-size: 14px;
}}
.table-fixed {{
  table-layout: fixed;
  width: 96vw;
  margin: 0 auto;
  font-size: 14px;
  border-collapse: collapse;
  background: #fff;
  border: 1px solid #e9e9ef;
  border-radius: 13px;
  box-shadow: 0 4px 20px 0 #f6f8fa;
  overflow: hidden;
}}
th, td {{
  font-size: 14px;
  padding: 5px 8px;
  background: #fff;
  border: 1px solid #ececec;
}}
th {{
  background: #f4f5f8;
  color: #2a3349;
  font-weight: 600;
}}
tr:nth-child(even) {{
  background: #f9fafc;
}}
tr:hover {{
  background: #f1f4fa;
}}
th.summary, td.summary {{
  width: 60%;
  min-width: 140px;
  max-width: 540px;
  vertical-align: top;
}}
th.origin, td.origin {{
  width: 18%;
  min-width: 50px;
  max-width: 95px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}}
th.date, td.date {{
  width: 11%;
  min-width: 67px;
  max-width: 74px;
  text-align: center;
  letter-spacing: -0.5px;
}}
td.origin a {{
  display: inline-block;
  vertical-align: middle;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  font-size: 14px;
}}
.summary-cell {{
  display: block;
  white-space: normal;
  line-height: 1.37;
}}
.pagination {{
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 4px;
  margin: 22px 0 30px 0;
  font-size: 15px;
}}
.pagination button {{
  background: #fff;
  border: 1px solid #dedede;
  color: #3678ff;
  font-weight: 600;
  padding: 4px 12px;
  margin: 0 1.5px;
  border-radius: 8px;
  cursor: pointer;
  transition: background 0.12s, color 0.12s, border 0.12s;
  min-width: 28px;
  outline: none;
}}
.pagination button.active,
.pagination button:active {{
  background: #3678ff;
  color: #fff;
  border: 1.2px solid #3678ff;
}}
.pagination button:disabled {{
  background: #fafbfc;
  color: #bbb;
  border: 1px solid #e4e4e4;
  cursor: not-allowed;
}}
</style>
</head>
<body>
<div id="scroll-top-anchor"></div>
<h1>AI 마크다운 요약 목록</h1>
<table border="1" cellspacing="0" cellpadding="4" class="table-fixed" id="main-table">
<thead>
<tr>
    <th class="summary">요약</th>
    <th class="origin">원본</th>
    <th class="date">날짜</th>
</tr>
</thead>
<tbody id="table-body">
{tbody_html}
</tbody>
</table>
<div class="pagination" id="pagination"></div>
<script>
const rowsPerPage = 20;
const tableBody = document.getElementById('table-body');
const pagination = document.getElementById('pagination');
const anchor = document.getElementById('scroll-top-anchor');

const allRows = Array.from(tableBody.querySelectorAll('tr'));
const totalRows = allRows.length;
const totalPages = Math.ceil(totalRows / rowsPerPage);

function renderPage(page) {{
    tableBody.innerHTML = '';
    const start = (page - 1) * rowsPerPage;
    const end = start + rowsPerPage;
    for (let i = start; i < end && i < totalRows; i++) {{
        tableBody.appendChild(allRows[i]);
    }}

    pagination.innerHTML = '';
    if (totalPages > 1) {{
        const btnPrev = document.createElement('button');
        btnPrev.textContent = '<';
        btnPrev.disabled = (page === 1);
        btnPrev.onclick = () => renderPage(page - 1);
        pagination.appendChild(btnPrev);

        // 최대 7개 페이지 버튼 (ex: ... 4 5 6 7 8 9 10 ...)
        let startPage = Math.max(1, page - 3);
        let endPage = Math.min(totalPages, page + 3);

        if (startPage > 1) {{
            let btn1 = document.createElement('button');
            btn1.textContent = '1';
            btn1.onclick = () => renderPage(1);
            pagination.appendChild(btn1);
            if (startPage > 2) {{
                let dots = document.createElement('span');
                dots.textContent = '...';
                dots.style.padding = '0 6px';
                dots.style.color = '#aaa';
                pagination.appendChild(dots);
            }}
        }}
        for (let p = startPage; p <= endPage; p++) {{
            let btn = document.createElement('button');
            btn.textContent = p;
            if (p === page) btn.classList.add('active');
            btn.onclick = () => renderPage(p);
            pagination.appendChild(btn);
        }}
        if (endPage < totalPages) {{
            if (endPage < totalPages - 1) {{
                let dots = document.createElement('span');
                dots.textContent = '...';
                dots.style.padding = '0 6px';
                dots.style.color = '#aaa';
                pagination.appendChild(dots);
            }}
            let btnLast = document.createElement('button');
            btnLast.textContent = totalPages;
            btnLast.onclick = () => renderPage(totalPages);
            pagination.appendChild(btnLast);
        }}

        const btnNext = document.createElement('button');
        btnNext.textContent = '>';
        btnNext.disabled = (page === totalPages);
        btnNext.onclick = () => renderPage(page + 1);
        pagination.appendChild(btnNext);
    }}

    // 페이지 이동 시 스크롤 맨 위로
    // (h1보다 위쪽에 scroll-top-anchor를 두면 h1도 안가려짐)
    anchor.scrollIntoView({{ behavior: "smooth" }});
}}
renderPage(1);
</script>
</body>
</html>
"""

with open(INDEX_FILE, 'w', encoding='utf-8') as f:
    f.write(html)
