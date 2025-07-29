#!/usr/bin/env python3
import sys
from pathlib import Path

def delete_copy_md_files(posts_dir: str = "/Users/ympark4/Desktop/doejason.github.io/posts") -> None:
    """
    posts_dir 폴더 내에 이름에 'copy'가 포함된 .md 파일을 찾아 삭제합니다.
    """
    p = Path(posts_dir)
    if not p.is_dir():
        print(f"Error: '{posts_dir}' 폴더를 찾을 수 없습니다.", file=sys.stderr)
        sys.exit(1)

    files = list(p.glob("*copy*.md"))
    if not files:
        print("삭제할 파일이 없습니다.")
        return

    for f in files:
        try:
            f.unlink()
            print(f"Deleted: {f}")
        except Exception as e:
            print(f"Failed to delete {f}: {e}", file=sys.stderr)

if __name__ == "__main__":
    delete_copy_md_files()
