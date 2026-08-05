#!/usr/bin/env python3
"""Generate products.xml RSS feed from Etsy products for Pinterest auto-publish."""
import json, urllib.request, datetime
from pathlib import Path
from xml.sax.saxutils import escape as xml_escape

ROOT = Path("/Users/macmini/datacrafted-blog")
OUT = ROOT / "products.xml"

def fetch_products():
    """Fetch active Etsy listings with images."""
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
    products = []
    for l in data.get('results', []):
        lid = l['listing_id']
        # image
        try:
            ireq = urllib.request.Request(f"https://api.etsy.com/v3/application/listings/{lid}/images", headers={
                'x-api-key': f"{env['ETSY_KEYSTRING']}:{env['ETSY_SHARED_SECRET']}",
                'Authorization': f"Bearer {env['ETSY_ACCESS_TOKEN']}"})
            imgs = json.loads(urllib.request.urlopen(ireq, timeout=30).read()).get('results', [])
            img = imgs[0].get('url_fullxfull') if imgs else ''
        except Exception:
            img = ''
        products.append({
            'title': l['title'],
            'link': f"https://www.etsy.com/listing/{lid}",
            'desc': (l.get('description') or '')[:200].replace('\n', ' '),
            'img': img,
            'date': datetime.date.today().isoformat(),
        })
    return products

def build_rss(products):
    import email.utils
    mapping = json.load(open(ROOT / 'redirect_map.json')) if (ROOT / 'redirect_map.json').exists() else {}
    SITE = "https://matthieulebasai-droid.github.io/datacrafted-blog"
    items = ""
    for p in products:
        # real image sizes via HEAD
        try:
            hreq = urllib.request.Request(p['img'], method='HEAD')
            hres = urllib.request.urlopen(hreq, timeout=15)
            length = hres.headers.get('Content-Length', '0')
            ctype = hres.headers.get('Content-Type', 'image/jpeg').split(';')[0]
        except Exception:
            length, ctype = '0', 'image/jpeg'
        title = xml_escape(p['title'][:95])
        desc = p['desc'].replace(']]>', ']]]]><![CDATA[>')
        pub = email.utils.formatdate(timeval=None, localtime=False)
        # local redirect URL (domain claimed on Pinterest) -> lands on Etsy
        lid = p['link'].rstrip('/').split('/')[-1]
        slug = mapping.get(lid)
        local_link = f"{SITE}/go/{slug}/" if slug else p['link']
        items += f"""  <item>
    <title>{title}</title>
    <link>{local_link}</link>
    <description><![CDATA[{desc}]]></description>
    <pubDate>{pub}</pubDate>
    <guid>{local_link}</guid>
    <enclosure url="{p['img']}" type="{ctype}" length="{length}"/>
  </item>
"""
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>DataCrafted Products</title>
    <link>https://matthieulebasai-droid.github.io/datacrafted-blog/</link>
    <description>DataCrafted digital products: spreadsheets, Notion templates and automation tools.</description>
    <atom:link href="https://matthieulebasai-droid.github.io/datacrafted-blog/products.xml" rel="self" type="application/rss+xml"/>
{items}  </channel>
</rss>
"""

if __name__ == "__main__":
    products = fetch_products()
    OUT.write_text(build_rss(products), encoding='utf-8')
    print(f"✅ {OUT} — {len(products)} produits")
