#!/usr/bin/env python3
"""Build datacrafted-blog static site: markdown -> dark-themed SEO HTML."""
import markdown
from pathlib import Path

ROOT = Path("/Users/macmini/datacrafted-blog")
POSTS = ROOT / "posts"
POSTS.mkdir(exist_ok=True)

ARTICLES = [
    {
        "src": "/Volumes/Cascade/Hermes/projects/tcm_v3/content/articles/article_01_zero_dependency.md",
        "slug": "zero-dependency-python-cli-tools",
        "title": "I Built 10 Free Python CLI Tools — Here's Why Zero-Dependency Matters",
        "desc": "Why 10 free open-source Python CLI tools run on nothing but the standard library — and why zero dependencies make a better product.",
        "date": "2026-07-31",
    },
    {
        "src": "/Volumes/Cascade/Hermes/projects/tcm_v3/content/articles/article_02_marketing_lessons.md",
        "slug": "six-months-digital-products-zero-sales",
        "title": "6 Months, 15 Tools, 3 Stores, 0 Sales — What I Learned Marketing Digital Products",
        "desc": "A transparent post-mortem of 6 months shipping developer tools: 15 tools, 3 stores, 0 sales — and the 7 marketing lessons learned the hard way.",
        "date": "2026-07-31",
    },
]

CSS = """
:root{--bg:#0d1117;--fg:#e6edf3;--muted:#8b949e;--accent:#58a6ff;--border:#30363d;--code-bg:#161b22}
*{box-sizing:border-box;margin:0;padding:0}
body{background:var(--bg);color:var(--fg);font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif;line-height:1.7;-webkit-font-smoothing:antialiased}
.wrap{max-width:760px;margin:0 auto;padding:2rem 1.25rem 4rem}
a{color:var(--accent);text-decoration:none}
a:hover{text-decoration:underline}
header.top{border-bottom:1px solid var(--border);margin-bottom:2.5rem;padding-bottom:1.5rem}
header.top h1{font-size:1.15rem;font-weight:700}
header.top h1 a{color:var(--fg)}
header.top .tagline{color:var(--muted);font-size:.9rem;margin-top:.25rem}
.post-meta{color:var(--muted);font-size:.85rem;margin-bottom:2rem}
article h1{font-size:1.9rem;line-height:1.25;margin-bottom:.75rem;letter-spacing:-.01em}
article h2{font-size:1.35rem;margin:2.25rem 0 1rem;padding-bottom:.4rem;border-bottom:1px solid var(--border)}
article h3{font-size:1.1rem;margin:1.75rem 0 .75rem}
article p{margin:0 0 1.1rem}
article ul,article ol{margin:0 0 1.1rem 1.5rem}
article li{margin:.35rem 0}
article code{background:var(--code-bg);border:1px solid var(--border);border-radius:5px;padding:.15rem .4rem;font-family:'SF Mono',ui-monospace,Menlo,Consolas,monospace;font-size:.85em}
article pre{background:var(--code-bg);border:1px solid var(--border);border-radius:8px;padding:1rem 1.15rem;overflow-x:auto;margin:0 0 1.2rem}
article pre code{background:none;border:none;padding:0;font-size:.85rem;line-height:1.55}
article hr{border:none;border-top:1px solid var(--border);margin:2rem 0}
article blockquote{border-left:3px solid var(--accent);padding:.4rem 1rem;color:var(--muted);margin:0 0 1.1rem}
article blockquote p{margin:0}
footer{border-top:1px solid var(--border);margin-top:3rem;padding-top:1.5rem;color:var(--muted);font-size:.85rem}
.card{display:block;border:1px solid var(--border);border-radius:10px;padding:1.4rem 1.5rem;margin-bottom:1.25rem;transition:border-color .15s ease;background:#11161d}
.card:hover{border-color:var(--accent);text-decoration:none}
.card h2{font-size:1.2rem;color:var(--fg);margin-bottom:.4rem}
.card p{color:var(--muted);font-size:.92rem;margin:0}
.card .date{color:var(--muted);font-size:.78rem;margin-top:.6rem;display:block}
.hero{margin-bottom:2.5rem}
.hero h1{font-size:2.1rem;letter-spacing:-.02em;line-height:1.2;margin-bottom:.75rem}
.hero p{color:var(--muted);font-size:1.05rem;max-width:600px}
.list-title{font-size:1.1rem;margin-bottom:1.25rem;color:var(--fg)}
@media(max-width:600px){.wrap{padding:1.25rem 1rem 3rem}article h1{font-size:1.55rem}.hero h1{font-size:1.7rem}}
"""

def page(title, desc, body, slug=None):
    canonical = f'<link rel="canonical" href="https://matthieulebasai-droid.github.io/datacrafted-blog/{slug}/">' if slug else ""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="p:domain_verify" content="8f5011c2f3629252bed463f94bbd39cd"/>
<title>{title}</title>
<meta name="description" content="{desc}">
{canonical}
<meta property="og:type" content="article">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta name="twitter:card" content="summary">
<meta name="color-scheme" content="dark">
<link rel="stylesheet" href="/datacrafted-blog/style.css">
</head>
<body>
<div class="wrap">
<header class="top">
<h1><a href="/datacrafted-blog/">DataCrafted</a></h1>
<div class="tagline">Python CLI tools & solo-dev lessons</div>
</header>
{body}
<footer>© 2026 DataCrafted · <a href="https://github.com/matthieulebasai-droid/datacrafted-tools">datacrafted-tools on GitHub</a> · <a href="/datacrafted-blog/">Home</a></footer>
</div>
</body>
</html>
"""

def md_to_html(src):
    return markdown.markdown(src, extensions=["fenced_code", "tables", "sane_lists"])

# Write shared stylesheet
(ROOT / "style.css").write_text(CSS)

# Build post pages
index_cards = ""
for a in ARTICLES:
    src = Path(a["src"]).read_text()
    # strip the markdown title (already in <title>/h1 of template? no — keep it in body)
    body = f'<article><div class="post-meta">{a["date"]} · DataCrafted</div>' + md_to_html(src) + "</article>"
    html = page(a["title"], a["desc"], body, slug=a["slug"])
    (POSTS / a["slug"]).mkdir(exist_ok=True)
    (POSTS / a["slug"] / "index.html").write_text(html)
    index_cards += f'<a class="card" href="/datacrafted-blog/posts/{a["slug"]}/"><h2>{a["title"]}</h2><p>{a["desc"]}</p><span class="date">{a["date"]}</span></a>\n'

# Build index page
index_body = f"""<div class="hero">
<h1>DataCrafted — build small, ship honest</h1>
<p>Field notes from building zero-dependency Python CLI tools, marketing digital products with $0 budget, and everything a solo developer learns the expensive way.</p>
</div>
<div class="list-title">Latest posts</div>
{index_cards}"""
(ROOT / "index.html").write_text(page("DataCrafted — Python CLI tools & solo-dev lessons", "Field notes from building zero-dependency Python CLI tools and marketing digital products with a $0 budget.", index_body))

print("Built:", sorted(str(p.relative_to(ROOT)) for p in [ROOT/"index.html", ROOT/"style.css", *(POSTS/a["slug"]/"index.html" for a in ARTICLES)]))
