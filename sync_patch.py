#!/usr/bin/env python3
"""Read Capcom official Steam announcements; flag newer battle changes for review.
This DOES NOT alter move frame data or combos. Designed for GitHub Actions/GitHub Pages.
"""
import json, re, urllib.request, datetime, pathlib
ROOT=pathlib.Path(__file__).resolve().parent
out=ROOT/'data/patch-status.json'
old=json.loads(out.read_text(encoding='utf8'))
now=datetime.datetime.now(datetime.timezone.utc).date().isoformat()
url='https://api.steampowered.com/ISteamNews/GetNewsForApp/v2/?appid=1364780&count=50&maxlength=2000&format=json'
try:
    req=urllib.request.Request(url,headers={'User-Agent':'RyuOkiLab-VersionWatch/1.0','Accept':'application/json'})
    with urllib.request.urlopen(req,timeout=20) as response: source=json.load(response)
    items=source['appnews']['newsitems']
    pattern=re.compile(r'\b(patch notes|battle (?:change|balance|adjustment)|balance (?:update|changes|adjustment)|bug fixes|gameplay changes)\b',re.I)
    relevant=[]
    for it in items:
        raw=(it.get('title','')+' '+re.sub(r'<[^>]+>',' ',it.get('contents','')))
        if pattern.search(raw):
            d=datetime.datetime.fromtimestamp(it['date'],datetime.timezone.utc).date().isoformat()
            relevant.append({'date':d,'title':it.get('title',''),'url':it.get('url',''),'mentions_ryu':bool(re.search(r'\bryu\b|リュウ|隆',raw,re.I))})
    relevant.sort(key=lambda x:x['date'],reverse=True)
    latest=relevant[0] if relevant else None
    if latest:
        old.update(last_checked=now,latest_official_news=latest['date'],headline=latest['title'],url=latest['url'],review_needed=latest['date']>'2026-08-03',items=relevant[:10])
    else:old.update(last_checked=now,headline='未在最近 50 条官方新闻中识别到平衡公告；无法据此断定没有更新',review_needed=True)
    old.pop('error',None)
except Exception as exc:
    old.update(last_checked=now,headline='官方公告自动检测失败；请人工核对 Capcom',review_needed=True,error=type(exc).__name__)
out.write_text(json.dumps(old,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print(old['headline'])
