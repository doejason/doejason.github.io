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
</style>
</head>
<body>
<h1>Markdown Files</h1>
<table border="1" cellspacing="0" cellpadding="4">
<thead>
<tr>
    <th>요약</th>
    <th>원본(markdown)</th>
    <th>날짜</th>
</tr>
</thead>
<tbody>
{''.join(rows)}
</tbody>
</table>

<div id="tooltip" class="tooltip-box"></div>
<script>
const tooltip = document.getElementById('tooltip');
let tooltipTimeout = null;

document.querySelectorAll('.summary-cell').forEach(cell => {{
  cell.addEventListener('mouseenter', function(e) {{
    tooltip.textContent = cell.getAttribute('data-summary');
    tooltip.style.display = 'block';
    const rect = cell.getBoundingClientRect();
    tooltip.style.left = (rect.left + window.scrollX) + 'px';
    tooltip.style.top = (rect.bottom + window.scrollY + 8) + 'px';
    tooltip.setAttribute('data-active', '1');
  }});
  cell.addEventListener('mouseleave', function(e) {{
    tooltipTimeout = setTimeout(() => {{
      if (!tooltip.matches(':hover')) {{
        tooltip.style.display = 'none';
        tooltip.removeAttribute('data-active');
      }}
    }}, 100);
  }});
}});

tooltip.addEventListener('mouseenter', function(e) {{
  if (tooltipTimeout) {{
    clearTimeout(tooltipTimeout);
    tooltipTimeout = null;
  }}
  tooltip.setAttribute('data-active', '1');
}});
tooltip.addEventListener('mouseleave', function(e) {{
  tooltipTimeout = setTimeout(() => {{
    tooltip.style.display = 'none';
    tooltip.removeAttribute('data-active');
  }}, 100);
}});
</script>
</body>
</html>
"""

with open(INDEX_FILE, 'w', encoding='utf-8') as f:
    f.write(html)
