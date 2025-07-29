import os

POSTS_DIR = 'posts'
INDEX_FILE = 'index.html'

md_files = sorted([f for f in os.listdir(POSTS_DIR) if f.endswith('.md')])

rows = []
for md in md_files:
    path = os.path.join(POSTS_DIR, md)
    with open(path, encoding='utf-8') as f:
        # 줄단위로 읽어서 코드블록 시작문자 제거
        lines = f.readlines()
        # 코드블록 시작("```markdown", "```") 있는 줄 모두 제외
        pure_lines = [line.strip() for line in lines if not (line.strip().startswith('```'))]
        # 남은 줄 합치기(개행→공백)
        content = ' '.join(pure_lines).strip()
        # 앞 20글자만 title로
        title = content[:20]
        rows.append(f'<li><a href="{path}">{title}...</a></li>')

html = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><title>Markdown List</title></head>
<body>
<h1>Markdown Files</h1>
<ul>
{''.join(rows)}
</ul>
</body></html>
"""

with open(INDEX_FILE, 'w', encoding='utf-8') as f:
    f.write(html)
