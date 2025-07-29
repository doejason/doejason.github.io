import os

POSTS_DIR = 'posts'
INDEX_FILE = 'index.html'

md_files = sorted([f for f in os.listdir(POSTS_DIR) if f.endswith('.md')])

rows = []
for md in md_files:
    # 파일 경로
    md_path = os.path.join(POSTS_DIR, md)
    txt_name = os.path.splitext(md)[0] + '.txt'
    txt_path = os.path.join(POSTS_DIR, txt_name)

    # 요약(txt) 내용 읽기
    if os.path.exists(txt_path):
        with open(txt_path, encoding='utf-8') as f:
            summary = f.read().strip().replace('\n', ' ')
            summary = summary[:80] + ('...' if len(summary) > 80 else '')
    else:
        summary = "(요약 없음)"

    # 원본(markdown) 링크
    md_link = f'<a href="{md_path}">{md}</a>'

    rows.append(f"<tr><td>{summary}</td><td>{md_link}</td></tr>")

# HTML 테이블 구조로 생성
html = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><title>Markdown List</title></head>
<body>
<h1>Markdown Files</h1>
<table border="1" cellspacing="0" cellpadding="4">
<thead>
<tr>
    <th>요약</th>
    <th>원본(markdown)</th>
</tr>
</thead>
<tbody>
{''.join(rows)}
</tbody>
</table>
</body></html>
"""

with open(INDEX_FILE, 'w', encoding='utf-8') as f:
    f.write(html)
