"""curriculums/ のMarkdownファイルを docs/ にコピーするビルドスクリプト。

日本語ディレクトリ・ファイル名を英語スラッグ（part-XX/chapter-XX/X-X-X.md）に変換し、
MkDocs のソースディレクトリ（docs/）に配置する。
教材内のセクション間リンクも新しいパスに書き換える。
"""

import re
import shutil
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parent.parent
CURRICULUMS_DIR = ROOT / "curriculums"
DOCS_DIR = ROOT / "docs"


def extract_part_slug(dirname: str) -> str:
    """'part-01_はじめに' → 'part-01'"""
    match = re.match(r"(part-\d+)", dirname)
    return match.group(1) if match else dirname


def extract_chapter_slug(dirname: str) -> str:
    """'chapter-01_この教材について' → 'chapter-01'"""
    match = re.match(r"(chapter-\d+)", dirname)
    return match.group(1) if match else dirname


def extract_section_slug(filename: str) -> str:
    """'1-1-1_なぜClaude Codeを使うのか.md' → '1-1-1.md'"""
    match = re.match(r"(\d+-\d+-\d+)", filename)
    return f"{match.group(1)}.md" if match else filename


def rewrite_links(content: str) -> str:
    """Markdown 内の日本語パスリンクを英語スラッグに書き換える。

    対象パターン:
      - ../../part-XX_日本語/chapter-XX_日本語/X-X-X_日本語.md
      - ../chapter-XX_日本語/X-X-X_日本語.md
      - X-X-X_日本語.md
    URL エンコード（%20 等）にも対応する。
    """

    def replace_link(match: re.Match) -> str:
        prefix = match.group(1)  # [text]( or (
        path = unquote(match.group(2))  # URL デコード
        suffix = match.group(3)  # ) or anchor

        # パスの各セグメントをスラッグに変換
        segments = path.split("/")
        new_segments = []
        for seg in segments:
            if seg == ".." or seg == ".":
                new_segments.append(seg)
            elif seg.startswith("part-"):
                new_segments.append(extract_part_slug(seg))
            elif seg.startswith("chapter-"):
                new_segments.append(extract_chapter_slug(seg))
            elif re.match(r"\d+-\d+-\d+", seg):
                new_segments.append(extract_section_slug(seg))
            else:
                new_segments.append(seg)

        return prefix + "/".join(new_segments) + suffix

    # Markdown リンク内のパスを書き換え: [text](path) or [text](path#anchor)
    pattern = r"(\[[^\]]*\]\()([^)#]+)((?:#[^)]*)?)\)"
    return re.sub(pattern, lambda m: replace_link(m) + ")", content)


def build_docs():
    # docs/ 内の part-* ディレクトリだけをクリーン（index.md は保持）
    if DOCS_DIR.exists():
        for item in DOCS_DIR.iterdir():
            if item.is_dir() and item.name.startswith("part-"):
                shutil.rmtree(item)

    # curriculums/ から docs/ にコピー（リンク書き換え付き）
    for part_dir in sorted(CURRICULUMS_DIR.iterdir()):
        if not part_dir.is_dir():
            continue
        part_slug = extract_part_slug(part_dir.name)

        for chapter_dir in sorted(part_dir.iterdir()):
            if not chapter_dir.is_dir():
                continue
            chapter_slug = extract_chapter_slug(chapter_dir.name)

            dest_dir = DOCS_DIR / part_slug / chapter_slug
            dest_dir.mkdir(parents=True, exist_ok=True)

            for md_file in sorted(chapter_dir.glob("*.md")):
                section_slug = extract_section_slug(md_file.name)
                dest_path = dest_dir / section_slug

                content = md_file.read_text(encoding="utf-8")
                content = rewrite_links(content)
                dest_path.write_text(content, encoding="utf-8")

    print(f"Done: copied curriculum files to {DOCS_DIR}")


if __name__ == "__main__":
    build_docs()
