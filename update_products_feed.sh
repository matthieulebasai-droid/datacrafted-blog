#!/bin/bash
# Daily Pinterest RSS feed update: regenerate products.xml + /go/ redirects, push if changed.
set -u
cd /Users/macmini/datacrafted-blog || exit 1

# 0. Refresh Etsy token first (expires every ~2h; non-interactive refresh)
cd /Volumes/Cascade/Hermes/etsy-shop || exit 1
/usr/bin/python3 etsy_oauth.py --refresh > /tmp/rss_token.log 2>&1 || true
cd /Users/macmini/datacrafted-blog || exit 1

# 1. Regenerate redirects + feed (stdlib only, works with system python)
if ! /usr/bin/python3 build_redirects.py > /tmp/rss_build.log 2>&1; then
  # API likely failed (token expiry) — keep the existing feed, stay silent
  exit 0
fi
if ! /usr/bin/python3 gen_products_rss.py >> /tmp/rss_build.log 2>&1; then
  exit 0
fi

# 2. Validate XML + item count before touching git
COUNT=$(/usr/bin/python3 -c "
import xml.etree.ElementTree as ET
try:
    r = ET.parse('products.xml')
    n = len(r.findall('.//item'))
    assert n >= 5, f'feed too small: {n}'
    print(n)
except Exception as e:
    print('ERR', e)
    exit(1)
" 2>/dev/null) || { echo "⚠️ products.xml invalide — flux NON mis à jour"; exit 1; }

# 3. Push only if changed
if git diff --quiet products.xml redirect_map.json go/ 2>/dev/null; then
  exit 0
fi
git add products.xml redirect_map.json go/ 2>/dev/null
git commit -m "Update products RSS feed ($(date +%F))" -q 2>/dev/null
git push -q origin HEAD 2>>/tmp/rss_build.log || { echo "⚠️ push GitHub échoué"; exit 1; }
echo "✅ products.xml mis à jour ($COUNT produits) — Pinterest épingle automatiquement"
