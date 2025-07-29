import os

POSTS_DIR = 'posts'
INDEX_FILE = 'index.html'

md_files = sorted([f for f in os.listdir(POSTS_DIR) if f.endswith('.md')])

rows = []
for md in md_files:
    path = os.path.join(POSTS_DIR, md)
    with open(path, encoding='utf-8') as f:
        content = f.read().replace('\n', ' ').strip()
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
