import re, sys
sys.stdout.reconfigure(encoding='utf-8')
with open('config/alias.txt','r',encoding='utf-8') as f:
    lines = f.readlines()
patterns = []
for l in lines:
    l = l.strip()
    if not l or l.startswith('#'): continue
    parts = l.split(',')
    main = parts[0].strip()
    for a in parts[1:]:
        a = a.strip()
        if not a: continue
        if a.startswith('re:'):
            patterns.append((main, re.compile(a[3:])))
        else:
            patterns.append((main, a))
def match(name):
    # 先精确匹配
    for main, p in patterns:
        if isinstance(p, str) and name == p: return main
    # 再正则（顺序敏感）
    for main, p in patterns:
        if isinstance(p, re.Pattern) and p.search(name): return main
    return None

# 测试：Pdtv后缀 + 基础匹配 + 防吞
tests = [
    # Pdtv后缀
    ('重温经典Pdtv', '重温经典'),
    ('TVBS新闻Pdtv', 'TVBS新闻'),
    ('TVBS欢乐Pdtv', 'TVBS欢乐'),
    ('TVBS精采Pdtv', 'TVBS精采'),
    ('TVBSPdtv', 'TVBS'),
    ('华视Pdtv', '华视'),
    ('华视新闻Pdtv', '华视新闻'),
    ('民视Pdtv', '民视'),
    ('民视综艺Pdtv', '民视综艺'),
    ('公视Pdtv', '公视'),
    ('公视3台Pdtv', '公视3台'),
    ('台视Pdtv', '台视'),
    ('中视Pdtv', '中视'),
    # 简繁 + 后缀
    ('東森新聞Pdtv', '东森新闻'),
    # 三立综艺 不在 demo.txt 中，暂不测试
    # ('三立綜藝Pdtv', '三立综艺'),
    ('緯來戲劇Pdtv', '纬来戏剧'),
    # TVB
    ('无线翡翠Pdtv', 'TVB翡翠'),
    ('无线明珠FYtv', 'TVB明珠'),
    ('无线星河Pdtv', 'TVB星河'),
    ('TVBPlusPdtv', 'TVBPlus'),
    ('Plus综合Pdtv', 'TVBPlus'),
    # 凤凰
    ('凤凰中文Pdtv', '凤凰中文'),
    ('凤凰资讯Pdtv', '凤凰资讯'),
    ('凤凰香港Pdtv', '凤凰香港'),
    # 其他
    ('澳亚卫视Pdtv', '澳亚卫视'),
    ('ViuTVPdtv', 'ViuTV'),
    ('NOW新闻Pdtv', 'NOW新闻台'),
    ('深圳财经生活Pdtv', '深圳财经生活'),
    ('汕头文旅Pdtv', '汕头文旅'),
    ('金鹰纪实Pdtv', '金鹰纪实'),
    ('魅力足球Pdtv', '魅力足球'),
    ('RTHK31Pdtv', 'RTHK31'),
    ('大湾区卫视Pdtv', '大湾区卫视'),
    ('卡酷少儿Pdtv', '卡酷少儿'),
    ('哒啵电竞Pdtv', '哒啵电竞'),
    ('游戏风云Pdtv', '游戏风云'),
    ('五星体育Pdtv', '五星体育'),
    # 原有Pdtv频道（精确匹配应优先）
    ('有线新闻FYtv', '有线新闻'),
    ('无线翡翠FYtv', 'TVB翡翠'),
    ('无线娱乐FYtv', 'TVB娱乐新闻'),
    ('无线千禧FYtv', 'TVB千禧经典'),
]

fail = 0
for src, expected in tests:
    r = match(src)
    ok = r == expected
    if not ok:
        print(f"FAIL {src:<30} expected={expected} got={r}")
        fail += 1

if fail == 0:
    print(f"ALL {len(tests)} PASS ✓")
else:
    print(f"{fail}/{len(tests)} FAILED")
