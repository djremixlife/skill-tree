#!/usr/bin/env python3
# 技能樹每月健檢：驗證公開頁存活 + 讀技能數 → 推 Discord
import os, json, urllib.request, urllib.error, datetime

URL = "https://djremixlife.github.io/skill-tree/"

def http_code(u):
    try:
        return urllib.request.urlopen(u, timeout=20).getcode()
    except urllib.error.HTTPError as e:
        return e.code
    except Exception:
        return 0

code = http_code(URL)
try:
    count = len(json.load(open("catalog.json"))["skills"])
except Exception:
    count = "?"
date = (datetime.datetime.utcnow() + datetime.timedelta(hours=8)).strftime("%Y-%m-%d")
status = "✅ 公開頁 200 OK" if code == 200 else f"⚠️ 公開頁異常 HTTP {code}"
msg = (f"🌲 **技能樹每月健檢**（{date}）\n"
       f"{status}｜{URL}\n"
       f"📦 收錄技能：{count}\n"
       f"🔔 這個月有裝新 skill 的話，本機跟 Claude 說「更新技能樹」補卡片。\n"
       f"（雙棲健檢／pro-kit07 需本機新鮮資料，另跑）")

hook = os.environ.get("DISCORD_WEBHOOK")
if not hook:
    raise SystemExit("缺 DISCORD_WEBHOOK secret")
data = json.dumps({"username": "🌲 技能樹維護", "content": msg}).encode()
req = urllib.request.Request(hook, data=data, headers={"Content-Type": "application/json", "User-Agent": "SkillTreeBot/1.0 (+github-actions)"})
urllib.request.urlopen(req, timeout=20)
print(f"Discord sent. page={code} count={count}")
