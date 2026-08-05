#!/usr/bin/env python3
"""Generate /go/<slug>/ redirect pages for each product + update RSS links."""
import json, re, urllib.request
from pathlib import Path

ROOT = Path("/Users/macmini/datacrafted-blog")
GO = ROOT / "go"
SITE = "https://matthieulebasai-droid.github.io/datacrafted-blog"

def slugify(title):
    s = title.lower()
    s = re.sub(r'[^a-z0-9]+', '-', s).strip('-')
    return s[:60].rstrip('-')

def load_products():
    env = {}
    with open('/Volumes/Cascade/Hermes/.env') as f:
        for line in f:
            if line.strip() and not line.startswith('#') and '=' in line:
                k, v = line.strip().split('=', 1)
                env[k.strip()] = v.strip()
    url = f"https://api.etsy.com/v3/application/shops/{env['ETSY_SHOP_ID']}/listings/active?limit=100"
    req = urllib.request.Request(url, headers={
        'x-api-key': f"{env['ETSY_KEYSTRING']}:{env['ETSY_SHARED_SECRET']}",
        'Authorization': f"Bearer {env['ETSY_ACCESS_TOKEN']}"})
    data = json.loads(urllib.request.urlopen(req, timeout=30).read())
    return [(l['listing_id'], l['title']) for l in data.get('results', [])]

def redirect_page(slug, listing_id, title):
    target = f"https://www.etsy.com/listing/{listing_id}"
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta http-equiv="refresh" content="0;url={target}">
<link rel="canonical" href="{target}">
<title>{title}</title>
</head>
<body>
<p>Redirecting to <a href="{target}">the product on Etsy</a>...</p>
</body>
</html>
"""

def main():
    products = load_products()
    print(f"{len(products)} produits")
    mapping = {}
    for lid, title in products:
        slug = slugify(title)
        # ensure unique slugs
        base, i = slug, 2
        while slug in mapping.values():
            slug = f"{base}-{i}"
            i += 1
        mapping[lid] = slug
        page = GO / slug / "index.html"
        page.parent.mkdir(parents=True, exist_ok=True)
        page.write_text(redirect_page(slug, lid, title[:90]), encoding='utf-8')
        print(f"  {slug} → etsy.com/listing/{lid}")
    # Save mapping for RSS generator
    json.dump(mapping, open(ROOT / 'redirect_map.json', 'w'))
    print(f"✅ {len(mapping)} pages de redirection générées")

if __name__ == "__main__":
    main()
