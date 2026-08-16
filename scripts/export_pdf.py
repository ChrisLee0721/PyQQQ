"""把 docs/test-report.md 转成 PDF。

链路：markdown → HTML（含 CJK 样式）→ Edge headless 打印为 PDF。
图片用相对路径（HTML 与 MD 同目录，figures/ 相对路径自动解析）。

产出：docs/test-report.html、docs/test-report.pdf

用法：
    .venv/Scripts/python.exe scripts/export_pdf.py
"""

import os
import subprocess

import markdown

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MD = os.path.join(HERE, "docs", "test-report.md")
HTML = os.path.join(HERE, "docs", "test-report.html")
PDF = os.path.join(HERE, "docs", "test-report.pdf")

EDGE_PATHS = [
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
]

CSS = """
<style>
  :root { --border: #d0d7de; --muted: #57606a; }
  * { box-sizing: border-box; }
  body {
    font-family: "Microsoft YaHei", "SimHei", "PingFang SC", "Noto Sans CJK SC", sans-serif;
    font-size: 13px; line-height: 1.6; color: #1f2328;
    max-width: 900px; margin: 0 auto; padding: 24px 32px;
  }
  h1 { font-size: 24px; border-bottom: 2px solid var(--border); padding-bottom: 8px; }
  h2 { font-size: 19px; border-bottom: 1px solid var(--border); padding-bottom: 6px; margin-top: 28px; }
  h3 { font-size: 15px; margin-top: 20px; }
  h4 { font-size: 13.5px; margin-top: 16px; }
  table { border-collapse: collapse; width: 100%; margin: 14px 0; font-size: 12px; }
  th, td { border: 1px solid var(--border); padding: 6px 10px; text-align: left; }
  th { background: #f6f8fa; font-weight: 600; }
  tr:nth-child(even) td { background: #fafbfc; }
  code {
    font-family: Consolas, "Courier New", monospace;
    background: #eff1f3; padding: 1px 5px; border-radius: 4px; font-size: 12px;
  }
  pre { background: #f6f8fa; padding: 12px 14px; border-radius: 6px; overflow-x: auto; }
  pre code { background: none; padding: 0; }
  blockquote {
    border-left: 4px solid #d0d7de; margin: 12px 0; padding: 2px 14px;
    color: var(--muted); background: #fafbfc;
  }
  img { max-width: 100%; height: auto; border: 1px solid var(--border); border-radius: 6px; }
  hr { border: none; border-top: 1px solid var(--border); margin: 24px 0; }
  @page { size: A4; margin: 18mm 15mm; }
</style>
"""


def main():
    with open(MD, encoding="utf-8") as f:
        md_text = f.read()

    body = markdown.markdown(
        md_text,
        extensions=["tables", "fenced_code", "toc", "sane_lists"],
    )
    html = (
        "<!DOCTYPE html><html lang='zh-CN'><head><meta charset='utf-8'>"
        f"<title>QuoNic 测试报告书</title>{CSS}</head><body>{body}</body></html>"
    )
    with open(HTML, "w", encoding="utf-8") as f:
        f.write(html)
    print("已写入", HTML)

    edge = next((p for p in EDGE_PATHS if os.path.exists(p)), None)
    if edge is None:
        raise FileNotFoundError("未找到 Edge，请手动用浏览器打开 HTML 后打印为 PDF")

    url = "file:///" + HTML.replace("\\", "/")
    subprocess.run(
        [
            edge, "--headless", "--disable-gpu", "--no-pdf-header-footer",
            f"--print-to-pdf={PDF}", url,
        ],
        check=True, timeout=120,
    )
    print("已写入", PDF)


if __name__ == "__main__":
    main()
